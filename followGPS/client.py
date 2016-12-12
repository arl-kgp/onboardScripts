import zmq
import sys
import time

context = zmq.Context()

sock = context.socket(zmq.REQ)
sock.connect("tcp://127.0.0.1:5678")
while True:
    sock.send('y')
    print 'Pos:', sock.recv()
    time.sleep(1)
