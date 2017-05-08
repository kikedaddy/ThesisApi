import socket
import sys
import struct
import threading
import message_pb2
import movement_pb2


RHOST = ""
RPORT = 8888

class SSender:
	speed = 0
	angle = 0
	def __init__(self, speed, angle):
		self.speed = speed
		self.angle = angle
	def send_msg(self, sock, msg):
		# Prefix each message with a 4-byte length (network byte order)
		msg = struct.pack('>I', len(msg)) + msg
		sock.sendall(msg)

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

	def send_loop(self, sock):
		
		while 1:
			sending = movement_pb2.Move()
			#if sending.steering != self.gangle and sending.movement != self.gspeed:

			sending.steering = self.angle #value from ROS
			sending.movement = self.speed #value from ROS

			#print str(sending.steering) + ", " + str(self.gangle) + ", " + str(sending.movement) + ", " + str(self.gspeed)

			send_str = sending.SerializeToString()

			#sock.send(send_str)
			self.send_msg(sock, send_str)
		sock.close()

	def setSpeed(self, speed):
		self.speed = speed

	def setAngle(self, angle):
		self.angle = angle


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