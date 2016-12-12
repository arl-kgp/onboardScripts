import threading
import socket
import zmq

pos = '22,22'

class Server (threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        global pos
        s = socket.socket()
        s.bind(("0.0.0.0", 8082))
        s.listen(5)
        c, addr = s.accept()    # waits till it connects
        while True:
            message = c.recv(1024)      # recv pos
            if message == '':
                pass
            else:
                pos = message
                
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
server.daemon = True
zmqserver = Serverzmq()
zmqserver.daemon = True
server.start()
zmqserver.start()
