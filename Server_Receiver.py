import socket
import sys
from sys import getsizeof
import cv2
import time
import struct
import threading
import message_pb2
import movement_pb2
import numpy as np
#

HOST = '' #An available interface
PORT = 8887 #Any port

class SReceiver:
	image = ""

	def __init__(self):
		self.connect()

	def recv_msg(self, sock):
		# Read message length and unpack it into an integer
		raw_msglen = self.recvall(sock, 4)
		if not raw_msglen:
			return None
		msglen = struct.unpack('>I', raw_msglen)[0]
		# Read the message data
		return self.recvall(sock, msglen)

	def recvall(self, sock, n):
		# Helper function to recv n bytes or return None if EOF is hit
		data = ''

		while len(data) < n:
			packet = sock.recv(n - len(data))

			if not packet:
				return None
			data += packet
		return data

	def connect(self):
		self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		print 'Socket created'

		#Bind to addr/port
		try:
			self.s.bind((HOST, PORT))
		except socket.error as msg:
			print 'Bind failed: ' + str(msg[0]) + ' with message: ' + msg[1]
			sys.exit()

		print 'Socket bind successful'

		#Start listening on socket
		self.s.listen(10)
		print ' Socket is listening'

		#return conn, addr	#Could include socket in return

	def recv_msg_loop(self):
		#Wait to accept connection
		conn, addr = self.s.accept()
		while 1:
			#data = conn.recv(1024)	#Random size(1024) AND ADDED CONCAT
			#print 'Before recv_msg'
			#Get the data from the socket. First 4bits are the length of the packet.
			data = self.recv_msg(conn)

			if data is None:
				break

			#To return the image as a string
			self.image = data

			#Get protobuf format
			proto_img = message_pb2.Image()

			#Parse proto message
			proto_img.ParseFromString(data)

			#Decode message with OpenCV
			nparr = np.fromstring(proto_img.pic, np.uint8)
			dec_img = cv2.imdecode(nparr, 1)

			#Show the image with OpenCV
			cv2.imshow("Image window", dec_img)
			cv2.waitKey(3)

			#conn.send('You are connected...')

		#conn.close() #Cannot close at this time

	def getImage(self):
		return self.image

#receiver = SReceiver()

#conn, addr = receiver.connect()

#print 'Got here!'

#receiver.recv_msg_loop()

#t1 = threading.Thread(target=receiver.recv_msg_loop, args=(conn, addr))
#t1.daemon = True
