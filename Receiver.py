import rospy
import socket
import struct
import cv2
import numpy as np
import sys
import unicodedata
from sys import getsizeof
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
import movement_pb2
import threading
import time
from geometry_msgs.msg import Twist
#

listenPort = 8888
listenAddress = ''
max_listen = 10

#The Receiver class is responsible for receiving speed and angle values from the 
#SSender and publishing them to ROS.
#The Receiver represents the ROS library.
class Receiver(threading.Thread):
	def __init__(self):
		self.speed = 0
		self.angle = 0
		self.setupSockets()
		self._stop_event = threading.Event()
		rospy.init_node('Receiver', anonymous=False)
		# What function to call when you ctrl + c    
		rospy.on_shutdown(self.shutdown)
		self.cmd_vel = rospy.Publisher('cmd_vel_mux/input/navi', Twist, queue_size=10)

	def stop(self):
		self._stop_event.set()
	def stopped(self):
		return self._stop_event.is_set()
	def run(self):
		if (self.stopped() == False):
			#self._Thread__target(*self._Thread__args, **self._Thread__kwargs)
			self.receiveServer()
	def setupSockets(self):
		#Start the receiving socket
		self.sockrec = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.sockrec.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		try:
			self.sockrec.bind((listenAddress, listenPort))
			self.sockrec.listen(max_listen)
		except socket.error as msg:
			print "Connection failed"
			sys.exit()

	def receiveServer(self):
		#print "Enters recieveServer!"
		conn, addr = self.sockrec.accept()
		#print "GETS HERE"
		
		while not rospy.is_shutdown():
			#Get the data from the socket. First 4bits are the length of the packet.
			data = self.recv_msg(conn)

			if data is None:
				break

			#print "connected with " + addr[0] + ":" + str(addr[1]) + ", received: " + str(data)
			
			move_cmd = self.makeCmd(data)

			if move_cmd != None:
				self.cmd_vel.publish(move_cmd)

	def makeCmd(self, str_proto):
		cmd = movement_pb2.Move()
		cmd.ParseFromString(str_proto)

		if self.speed != cmd.movement and self.angle != cmd.steering:
			move_cmd = Twist()
			move_cmd.linear.x = cmd.movement
			move_cmd.angular.z = cmd.steering		
			self.speed = move_cmd.linear.x
			self.angle = move_cmd.angular.z
			#print "Different"
			return move_cmd
		else:
			return None


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

	def shutdown(self):
		print "Shutdown"
		self.sockrec.close()
		# a default Twist has linear.x of 0 and angular.z of 0.  So it'll stop TurtleBot
		self.cmd_vel.publish(Twist())
		# sleep just makes sure TurtleBot receives the stop command prior to shutting down the script
		rospy.sleep(1)

	def getSpeed(self):
		return self.speed

	def getAngle(self):
		return self.angle

#receiver = Receiver()
#receiver.receiveServer()