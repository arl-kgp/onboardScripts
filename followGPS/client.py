	
#!/usr/bin/env python
import socket
from threading import *
import time

serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = "0.0.0.0"
port = 8000
print (host)
print (port)
serversocket.bind((host, port))

class client(Thread):
    def __init__(self, socket, address):
        Thread.__init__(self)
        self.sock = socket
        self.addr = address
        self.start()

    def run(self):
        while 1:
            pos = self.sock.recv(1024)
            if pos[0] == 'A' or pos[0] == 'H':
            	gps = pos[1:].split(',')
            	latlong = gps[0]+','+gps[1]+' at '+gps[2]+'m'
            	print latlong
            	self.sock.send(latlong)
            elif pos[0] == 'B' :
            	gps_points = pos[1:].split('B')
            	for gps in gps_points :
            		latlong = gps.split(',')
            		print latlong[0] + ',' + latlong[1]+' at '+latlong[2]+'m'
            else :
            	print pos
            self.sock.send('22.318426,87.30438\n')

def sent():
	while True:
		clientsocket.send('22.318426,87.30438\n')
		time.sleep(0.1)
		#print 'Sending !\n'

serversocket.listen(5)
print ('server started and listening')
while 1:
    clientsocket, address = serversocket.accept()
    client(clientsocket, address)
    Thread(target=sent).start()
