from slapjack import slapjack
import ipc as ipc
import recognizer as recognizer
from time import sleep
import time

socket_path = "/tmp/slapjack.pyserver"

LINK = "LINK"
SET_READY = "SET_READY"
SET_SIMPLE_DEAL = "SIMPLE_DEAL"
SET_DEAL = "DEAL"
SET_HIT = "HIT"
SET_FAKE_HIT = "FAKE_HIT"

CONN_FAILED = "CONN_FAILED"
RUN_SUCCESS = "RUN_SUCCESS"
ARDUINO_FAILED = "ARDUINO_FAILED"

player = slapjack()
result = 0

def exitHandler():
    if ipc.server:
        ipc.server.shutdown(ipc.socket.SHUT_RDWR)
        ipc.server.close()

import atexit
atexit.register(exitHandler)

ipc.start(socket_path)
try:
    recognizer.init_camera()
    recognizer.init_recognizer()
except Error as e:
    print("Static error")
    print(e)
    exit(1)

def ipcHandler(conn, data):
    global result, player
    if data == LINK:
        r =recognizer.init_arduino()
        if r == -2:
            conn.send(ARDUINO_FAILED)
        elif r == -1:
            conn.send(CONN_FAILED)
        else:
            conn.send(RUN_SUCCESS)
        return

    if not recognizer.test():
        print("Arduino connection Failed")
        conn.send(CONN_FAILED)
        return

    if data == SET_READY:
        recognizer.set_ready()

        conn.send(RUN_SUCCESS)

        stime = time.time()
        recognizer.capture()
        result = recognizer.recognize()
        etime = time.time()
        return

    if data == SET_SIMPLE_DEAL:
        recognizer.set_deal()
        recognizer.set_ready()
        conn.send(RUN_SUCCESS)
        recognizer.capture()
        result = recognizer.recognize()
        return

    if data == SET_DEAL:
        recognizer.set_deal()

        action = player.if_slap(result)
        if action == SET_HIT:
            recognizer.hit()
        elif action == SET_FAKE_HIT:
            recognizer.fake_hit()

        player.increment()

        conn.send(str(result))
        recognizer.set_ready()
        recognizer.capture()
        result = recognizer.recognize()
        return

ipc.callback = ipcHandler

ipc.listen(ipc.one_time)


