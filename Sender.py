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
#

sendPort = 8887
sendAddress = ''		#'83.248.104.77'
max_listen = 10

class Sender:
	def __init__(self):
		self.bridge = CvBridge()
		#Setup Socket
		self.setupSockets()
		rospy.on_shutdown(self.shutdown)
		rospy.init_node('Sender')
		###
		###---ADDED NOW---
		###
		#rospy.init_node('Sender')
		#Subscribe to the image
		#while not rospy.is_shutdown():
		#self.image_sub = rospy.Subscriber('camera/rgb/image_raw', Image, self.imgCallback)
		#senderLoop()

	def setupSockets(self):
		#Start the receiving socket
		try:
			self.socksend = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			self.socksend.connect((sendAddress,sendPort))
		except socket.error as msg:
			print "Connection failed: " + str(msg)
			sys.exit()

	def imgCallback(self, msg):
		#Convert Ros Image to CV Image
		try:
			cv_image = self.bridge.imgmsg_to_cv2(msg, "bgr8")
		except CvBridgeError as e:
			print("Error converting image: " + e)
		#Encode Image
		encode_param=[int(cv2.IMWRITE_JPEG_QUALITY),50]
		result,encimg=cv2.imencode('.jpg',cv_image,encode_param)
		#Convert encoded image to string
		img_str = encimg.tostring()
		#Get img info
		(rows,cols,channels) = cv_image.shape
		send_str = self.makeProtoStr(rows,cols,channels,img_str)
		self.send_msg(send_str)
		
		nparr = np.fromstring(img_str, np.uint8) 		#########Take Away
		dec_img = cv2.imdecode(nparr,1)				########Take Away
		#cv2.imshow("Image window", dec_img)			#######Take Away
		#cv2.waitKey(3)								########TAKE AWAY

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
	    except socket.error as e:
	    	print "Error sending: " + str(e) 

	def shutdown(self):
		print "Shutdown"
		self.socksend.close()

	def senderLoop(self):
		#Subscribe to the image
		#while not rospy.is_shutdown():
		self.image_sub = rospy.Subscriber('camera/rgb/image_raw', Image, self.imgCallback)
		while not rospy.is_shutdown():
			time.sleep(0.001)



#rospy.init_node('Sender')
#sender = Sender()
#sender.senderLoop()
#while not rospy.is_shutdown():
#	time.sleep(0.001)
