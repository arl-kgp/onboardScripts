import zmq
import sys

context = zmq.Context()

sock = context.socket(zmq.REQ)
sock.connect("tcp://127.0.0.1:5678")
while True:
    sock.send(raw_input('Get new pos(y/n): '))
    print 'Pos:', sock.recv()
