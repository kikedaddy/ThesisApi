import socket
import sys
import struct
import threading
import message_pb2
import movement_pb2


RHOST = "127.0.0.1"
RPORT = 8888

class SSender:
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

	def send_loop(self, sock, msg):
		sending = movement_pb2.Move()
		sending.steering = 1.5 #value from ROS
		sending.movement = 2.0 #value from ROS

		send_str = sending.SerializeToString()

		while 1:
			sock.send(send_str)
		sock.close()

sender = SSender()

sock = sender.send_connect(RHOST, RPORT)
print '2'
sending = movement_pb2.Move()
sending.steering = 0.5
sending.movement = 0
msg = sending.SerializeToString()

sender.send_loop(sock, msg)

#t2 = threading.Thread(target=sender.send_loop, args=(sock, msg))
#t2.daemon = True