#Sockets
import socket
import sys
from sys import getsizeof
import cv2
import time
import struct
import message_pb2
import numpy as np

HOST = '' #An available interface
PORT = 8888 #Any port

RHOST = '192.168.43.215'
RPORT = 8887

def recv_msg(sock):
    # Read message length and unpack it into an integer
    raw_msglen = recvall(sock, 4)
    if not raw_msglen:
        return None
    msglen = struct.unpack('>I', raw_msglen)[0]
    # Read the message data
    return recvall(sock, msglen)

def recvall(sock, n):
    # Helper function to recv n bytes or return None if EOF is hit
    data = ''
    while len(data) < n:
        packet = sock.recv(n - len(data))
        if not packet:
            return None
        data += packet
    return data

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
print 'Socket created'

#Bind to addr/port
try:
	s.bind((HOST, PORT))
except socket.error as msg:
	print 'Bind failed: ' + str(msg[0]) + ' with message: ' + msg[1]
	sys.exit()

print 'Socket bind successful'

#Start listening on socket
s.listen(10)
print ' Socket is listening'

#Wait to accept connection
conn, addr = s.accept()

while 1:
	#data = conn.recv(1024)	#Random size(1024) AND ADDED CONCAT

	#Get the data from the socket. First 4bits are the length of the packet.
	data = recv_msg(conn)

	print 'Connected with ' + addr[0] + ' : ' + str(addr[1])# + '. Received data: ' + str(data)

	#Get protobuf format
	proto_img = message_pb2.Image()

	print 'Size: ' + str(getsizeof(data))

	#Parse proto message
	proto_img.ParseFromString(data)

	print ''
	print('Width: ' + str(proto_img.rows) + ', Height: ' + str(proto_img.cols) + ', data: ' + str(proto_img.pic))
	print ''

	#Decode message with OpenCV
	nparr = np.fromstring(proto_img.pic, np.uint8)
	dec_img = cv2.imdecode(nparr, 1)

	#Show the image with OpenCV
	cv2.imshow("Image window", dec_img)
	cv2.waitKey(3)

#conn.send('You are connected...')

s.close()