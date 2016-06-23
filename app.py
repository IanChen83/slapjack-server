import './ipc.py' as ipc
import './recognizer.py' as recognizer
from time import sleep
import time

socket_path = "/tmp/slapjack.pyserver"

ipc.start(socket_path)
recognizer.init()

def ipcHandler(conn, data):
    if data == "set_ready":
        recognizer.set_ready()
        return

    if data == "simple_deal":
        recognizer.set_deal()
        recognizer.set_ready()
        return

    if data == "deal":
        stime = time.time()
        result = recognizer.recognize()
        etime = time.time()

        recognizer.deal()
        recognizer.set_ready()
        return

ipc.callback = ipcHandler

ipc.listen(ipc.one_time)


