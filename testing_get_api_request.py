##
## Sends a get request to the API and receives back a stream of images
##
import requests
import threading
import socket
import sys
import struct

url = "http://localhost/server.php?id=127.0.0.1"
IP = "127.0.0.1"
PORT = 10000
MAX_LISTEN = 100

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

#Bind to addr/port
try:
	s.bind((IP, PORT))
except socket.error as msg:
	print 'Bind failed: ' + str(msg[0]) + ' with message: ' + msg[1]
	sys.exit()

print 'Socket bind successful'

#Start listening on socket

#t1 = threading.Thread(target=s.listen, args=(10))
#t1.daemon = True

s.listen(10)
print ' Socket is listening'

#r = requests.get(url)
#print r.text

print "waiting for connection"
#Wait to accept connection
conn, addr = s.accept()

result = conn.recv(1024)
conn.send("I got the image!")

print result