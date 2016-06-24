import smbus
from time import sleep

import cv2
import pickle
import numpy as np
from picamera.array import PiRGBArray
from picamera import PiCamera
import smbus

bus = smbus.SMBus(1)
addr = 0x12
camera = None
rawCapture = None

thresholds = None

STOP      = 4
READY     = 5
ROLL_BACK = 6
DEAL      = 7
FAKE_HIT  = 8
HIT       = 9

def read():
    response = bus.read_byte(addr)
    return response

def write(byte):
    bus.write_byte(addr, byte)

def fake_hit():
    write(FAKE_HIT)

def hit():
    write(HIT)

def set_stop():
    write(STOP)

def set_ready():
    # Notice that this function is blocing
    print("SET_READY")
    msg = read()
    if msg == 1:
        write(READY)
        count = 0
        while read() != 2:
            count += 1
            if count > 20:
                break;
            sleep(1)
        return read() == 2
    elif msg == 2:
        return True

def set_rollback():
    write(ROLL_BACK)

def set_deal():
    msg = read()
    print("Message")
    print(msg)
    if msg == 2:
        write(DEAL)
    else:
        set_ready()
        write(DEAL)

def init_camera():
    global camera, rawCapture
    camera = PiCamera()
    camera.resolution = (1280, 720)

    rawCapture = PiRGBArray(camera)
    print("Recognizer: Camera initialized")

def init_recognizer(path = 'thresholds.pkl'):
    global thresholds
    thresholds = pickle.load(open(path, 'r'))
    print("Recognizer: Recognizer initialized")

def init_arduino():
    # Current behavior:
    # Arduino return 1 when serial is available

    print("Initialize Arduino connection")
    count = 0
    try:
        msg = read()
    except Error:
        print("Arduino connection failed")
        return -1
    if msg == 1:
        print("Arduino linked")
        set_ready()
        return 0
    elif msg == 2:
        print("Arduino ready to deal")
        return 0
    else:
        print("Adruino preparation failed")
        return -2

def test():
    try:
        msg = read()
    except:
        return False
    return True


def init():
    if(init_arduino() != 0):
        return -1
    init_camera()
    init_recognizer()

def capture(frame = rawCapture):
    if frame is None:
        print("Camera: invoke init_camera() first")
        return False
    print("Camera: Capture a frame")
    camera.capture(frame, format='bgr')

def recognize(raw = rawCapture):
    """
    frame: resolution (1280 x 720)

    return: number
    """
    if raw is None:
        print("Recognizer: invoke init_recognizer() first")
        return -1
    frame = raw.array
    target_area = frame[:300,450:900]

    imgray = cv2.cvtColor(target_area,cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(imgray,(5,5),20)
    test_th = \
    cv2.adaptiveThreshold(blur,255,cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY,35,2)

    contours, hierarchy = \
            cv2.findContours(test_th.copy(),cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=cv2.contourArea,reverse=True)[:3]

    x,y,w,h = cv2.boundingRect(contours[1])

    #tocompare = test_th[y:y+h, x:x+w]
    tocompare = cv2.resize(test_th[y:y+h, x:x+w],(400,250))

    diffs = [np.sum(tocompare-t) for t in thresholds]

    ret = np.argmin(diffs) + 1
    reset_frame(raw)
    return ret

def reset_frame(frame = rawCapture):
    frame.truncate(0)

