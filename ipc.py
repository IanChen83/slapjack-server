import socket
from time import sleep
import os

server = None
callback = None

def clear_socket_path(path):
    if os.path.exists(path):
        os.remove(path)

def start(path):
    global server
    clear_socket_path(path)
    server = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    server.bind(path)

def n_time_generator(n):
    def ret(data):
        if n < 0:
            yield False
        else:
            for x in range(n):
                yield True
            yield False
    return ret

one_time = n_time_generator(1)
def inf_time(data):
    while True:
        yield True

def listen(stopFunc = n_time_generator(2)):
    global server, callback
    # stopFunc should return a generator that:
    #    yield True if the data is None (only happening on first run)
    #    yield True if the data indicates continuing this connection
    #    yield False if the data indicates closing this connection

    if server is None:
        print("call 'start([path], [callback])' first!")
        return

    data = None
    for isStop in stopFunc(data):
        if not isStop:
            print("IPC server stop to listen")
            return
        print("IPC server listen for client")
        server.listen(1)

        conn, addr = server.accept()
        print("IPC server accept client")

        while True:
            # This is a blocking read.
            # If recv() return None, the connection is closed.

            # Note that the length of each message < 20

            data = conn.recv(20)
            if not data:
                print("IPC server connection closed by client")
                conn.close();
                break
            if callback:
                callback(conn, data)

def send(conn, data):
    conn.sendall(data)

if __name__ == '__main__':
    print("Directly invoke this script. Start testing")
    clear_socket_path()
    callback = send
    start()
    listen()
