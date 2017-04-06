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

HOST = '127.0.0.1' #An available interface
PORT = 8888 #Any port

class SReceiver:
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

		return conn, addr	#Could include socket in return

	def recv_msg_loop(self, conn, addr):
		print 'before loop'
		while 1:
			#data = conn.recv(1024)	#Random size(1024) AND ADDED CONCAT
			print 'Before recv_msg'
			#Get the data from the socket. First 4bits are the length of the packet.
			data = self.recv_msg(conn)

			print 'After recv_msg'

			if data is None:
				break

			#print 'Connected with ' + addr[0] + ' : ' + str(addr[1])# + '. Received data: ' + str(data)

			#Get protobuf format
			proto_img = message_pb2.Image()

			#print 'Size: ' + str(getsizeof(data))

			#Parse proto message
			proto_img.ParseFromString(data)

			#print('Width: ' + str(proto_img.rows) + ', Height: ' + str(proto_img.cols))# + ', data: ' + str(proto_img.pic))
			
			#Decode message with OpenCV
			nparr = np.fromstring(proto_img.pic, np.uint8)
			dec_img = cv2.imdecode(nparr, 1)

			#Show the image with OpenCV
			cv2.imshow("Image window", dec_img)
			cv2.waitKey(3)

			#conn.send('You are connected...')

		#conn.close() #Cannot close at this time

receiver = SReceiver()

conn, addr = receiver.connect()

print 'Got here!'

receiver.recv_msg_loop(conn, addr)

#t1 = threading.Thread(target=receiver.recv_msg_loop, args=(conn, addr))
#t1.daemon = True
