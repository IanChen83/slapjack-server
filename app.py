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
recognizer.init_camera()
recognizer.init_recognizer()

def ipcHandler(conn, data):
    global result, player
    if data == LINK:
        r = recognizer.init_arduino()
        if r == -1:
            conn.send(CONN_FAILED)
        else:
            conn.send(RUN_SUCCESS)
        return

    if data == SET_READY:
        if recognizer.set_ready():
            conn.send(RUN_SUCCESS)
            recognizer.capture(recognizer.rawCapture)
            result = recognizer.recognize(recognizer.rawCapture)
        else:
            conn.send(ARDUINO_FAILED)
        return

    if data == SET_SIMPLE_DEAL:
        recognizer.set_deal()
        recognizer.set_ready()
        conn.send(RUN_SUCCESS)
        recognizer.capture(recognizer.rawCapture)
        result = recognizer.recognize(recognizer.rawCapture)
        return

    if data == SET_DEAL:
        recognizer.set_deal()
        action = player.if_slap(result)
        if action == SET_HIT:
            recognizer.hit()
        elif action == SET_FAKE_HIT:
            recognizer.fake_hit()

        player.increment()

        #recognizer.set_ready()
        conn.send(str(result))
        #recognizer.capture(recognizer.rawCapture)
        #result = recognizer.recognize(recognizer.rawCapture)
        return

ipc.callback = ipcHandler

ipc.listen(ipc.one_time)


