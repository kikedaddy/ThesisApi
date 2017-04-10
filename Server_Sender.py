import socket
import sys
import struct
import threading
import message_pb2
import movement_pb2


#RHOST = "127.0.0.1"
#RPORT = 8888

class SSender:
	def __init__(self, IP, PORT):
		self.sockSend = self.send_connect(IP, PORT)



	def send_cmd(self, steering, movement):
		# Prefix each message with a 4-byte length (network byte order)
		msg = self.create_msg(steering, movement)
		msg = struct.pack('>I', len(msg)) + msg
		self.sockSend.sendall(msg)

	def send_connect(self, addr, port):
		s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s2.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

		print 'Addr: ' + str(addr) + ", Port: " + str(port)

		#Connect to host/port
		try:
			s2.connect((addr, port))
		except socket.error as msg:
			print 'Connection failed: ' + str(msg[0]) + ' with message: ' + msg[1]
			sys.exit()

		print 'got here'

		return s2

	def create_msg(self, steering, movement):
		sending = movement_pb2.Move()
		sending.steering = steering
		sending.movement = movement

		return sending.SerializeToString()

