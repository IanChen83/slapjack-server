import './ipc.py' as ipc
import './recognizer.py' as recognizer
from time import sleep
import time

socket_path = "/tmp/slapjack.pyserver"

ipc.start(socket_path)
recognizer.init()

def shake():


def ipcHandler(conn, data):
    if data == "set_ready":
        recognizer.set_ready()
        return
    if data == "simple_deal":
        recognizer.set_deal()
        recognizer.set_ready()
        return
    if data == "deal":
        # Don't know why this loop is needed......
        while recognizer.read() != 2:
            sleep(0.1)

        stime = time.time()
        result = recognizer.recognize()
        etime = time.time()

        recognizer.deal()

        # Don't know why this loop is needed, either......
        while recognizer.read() != 1:
            sleep(0.1)

        recognizer.set_ready()

ipc.callback = ipcHandler

ipc.listen()
