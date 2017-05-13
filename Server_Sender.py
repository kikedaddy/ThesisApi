import socket
import sys
import struct
import threading
import message_pb2
import movement_pb2
import time
#

RHOST = ""
RPORT = 8888

#The SSender class is responsible for sending speed and angle data to the ROS framework.
#The SSender represents the first abstraction layer of the API
#(Which is now glued together with Receiver on the same machine)
class SSender:
	def __init__(self):
		self.running = True
		self.send_connect("localhost", 8888)

	def send_msg(self, msg):
		# Prefix each message with a 4-byte length (network byte order)
		msg = struct.pack('>I', len(msg)) + msg
		self.sock.sendall(msg)

	def terminator(self):
		self.running = False


	def isRunning(self):
		return self.running

	def send_loop(self):
		while self.running:
			time.sleep(0.001)

	def send_connect(self, addr, port):
		s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s2.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

		#Connect to host/port
		try:
			s2.connect((addr, port))
		except socket.error as msg:
			print 'Connection failed: ' + str(msg[0]) + ' with message: ' + msg[1]
			sys.exit()

		self.sock = s2

	def setSpeed(self, speed):
		sending = movement_pb2.Move()
		sending.movement = speed #value from ROS
		send_str = sending.SerializeToString()
		self.send_msg(send_str)

	def setAngle(self, angle):
		sending = movement_pb2.Move()
		sending.movement = angle #value from ROS
		send_str = sending.SerializeToString()
		self.send_msg(send_str)

#sender = SSender()

#sock = sender.send_connect(RHOST, RPORT)
#print '2'
#sending = movement_pb2.Move()
#sending.steering = 0.5
#sending.movement = 0
#msg = sending.SerializeToString()
#msg = "lol"
#print '3'
#sender.send_loop(sock, 0.5, 0.5)

#t2 = threading.Thread(target=sender.send_loop, args=(sock, msg))
#t2.daemon = True
#t2.start()