import rospy
import socket
import SocketParser
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

#listenPort = 8887
#listenAddress = ''
#max_listen = 1

class Receiver:
	def __init__(self, socketIP, socketPort, maxListen):
		rospy.init_node('Receiver', anonymous=False)
		self.setupSockets(socketIP, socketPort, maxListen)
		# What function to call when you ctrl + c    
		rospy.on_shutdown(self.shutdown)
		self.cmd_vel = rospy.Publisher('cmd_vel_mux/input/navi', Twist, queue_size=10)
		#self.receiveServer()

	def setupSockets(self, socketIP, socketPort, maxListen):
		#Start the receiving socket
		self.sockrec = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.sockrec.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		try:
			self.sockrec.bind((socketIP, socketPort))
			self.sockrec.listen(maxListen)
		except socket.error as msg:
			print "Connection failed"
			sys.exit()

	def receiveServer (self):
		print "Enters recieveServer!"
		conn, addr = self.sockrec.accept()
		print "GETS HERE"
		
		while not (rospy.is_shutdown() or self.offline):
			#Get the data from the socket. First 4bits are the length of the packet.
			data = SocketParser.recv_msg(conn)

			if data is None:
				self.shutdown()
			else:
				print "connected with " + addr[0] + ":" + str(addr[1]) + ", received: " + str(data)
				move_cmd = self.makeCmd(data)
				self.cmd_vel.publish(move_cmd)

	def makeCmd(self, str_proto):
		cmd = movement_pb2.Move()
		cmd.ParseFromString(str_proto)
		move_cmd = Twist()
		move_cmd.linear.x = cmd.movement
		move_cmd.angular.z = cmd.steering
		return move_cmd

	def shutdown(self):
		print "Shutdown"
		self.sockrec.close()
		# a default Twist has linear.x of 0 and angular.z of 0.  So it'll stop TurtleBot
		self.cmd_vel.publish(Twist())
		# sleep just makes sure TurtleBot receives the stop command prior to shutting down the script
		rospy.sleep(1)
		self.offline = True

#receiver = Receiver()
#receiver.receiveServer()