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
import message_pb2
import threading
import time

#sendPort = 8888
#sendAddress = '83.248.104.77'

class Sender:
	def __init__(self, socketIP, socketPort):
		rospy.init_node('Sender', anonymous = False)

		self.bridge = CvBridge()
		#Setup Socket
		self.setupSockets(socketIP, socketPort)
		rospy.on_shutdown(self.shutdown)
		#Subscribe to the image
		self.image_sub = rospy.Subscriber('camera/rgb/image_raw', Image, self.imgCallback)
		self.start()

	def setupSockets(self, socketIP, socketPort):
		#Start the receiving socket
		try:
			self.socksend = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			self.socksend.connect((socketIP,socketPort))
		except socket.error as msg:
			print "Connection failed"
			sys.exit()

	def imgCallback(self, msg):
		#Convert Ros Image to CV Image
		try:
			cv_image = self.bridge.imgmsg_to_cv2(msg, "bgr8")
			#Encode Image
			encode_param=[int(cv2.IMWRITE_JPEG_QUALITY),50]
			result,encimg=cv2.imencode('.jpg',cv_image,encode_param)
			#Convert encoded image to string
			img_str = encimg.tostring()
			#Get img info
			(rows,cols,channels) = cv_image.shape
			
			send_str = self.makeProtoStr(rows,cols,channels,img_str)
			self.send_msg(send_str)
		except CvBridgeError as e:
			print("Error converting image: " + e)
		

	def makeProtoStr (self, rows,cols,channels,img_str):
		sending = message_pb2.Image()
		sending.rows = rows
		sending.cols = cols
		sending.channels = channels
		sending.pic = img_str
		return sending.SerializeToString()

	def send_msg(self, msg):
	    # Prefix each message with a 4-byte length (network byte order)
	    msg = struct.pack('>I', len(msg)) + msg
	    try:
	    	self.socksend.send(msg)
	    	self.recurrentError = 0
	    except socket.error as e:
	    	print "Error sending: " + str(e) 
	    	if (self.recurrentError >= 3):
	    		self.shutdown()
	    	else:
	    		self.recurrentError = self.recurrentError + 1

	def shutdown(self):
		print "Shutdown"
		self.socksend.close()
		self.offline = True



#sender = Sender()
	def start(self):
		while not (rospy.is_shutdown() or self.offline):
			time.sleep(0.001)
