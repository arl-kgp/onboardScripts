import threading
import time
import socket
import zmq

pos = '22,22'

class Server (threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        s = socket.socket()
        host = socket.gethostname()
        port = 12345
        s.bind((host, port))
        s.listen(5)
        c = None
        while True:
            if c is None:
                c, addr = s.accept()    # wait till it connects
            else:
                pos = c.recv(1024)      # recv pos 

class Serverzmq (threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    def run(self):
        context = zmq.Context()

        sock = context.socket(zmq.REP)
        sock.bind("tcp://127.0.0.1:5678")
        while True:
            message = sock.recv()
            if message == 'y':  
                print 'Received request, sending new pos...', pos
                sock.send(pos)
            else:
                continue        


server = Server()
zmqserver = Serverzmq()
server.start()
zmqserver.start()

