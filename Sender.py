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

sendPort = 8888
sendAddress = '83.248.104.77'
max_listen = 10

class Sender:
	def __init__(self):
		self.bridge = CvBridge()
		#Setup Socket
		self.setupSockets()
		rospy.on_shutdown(self.shutdown)
		self.n = 0					####Take Away!
		#Subscribe to the image
		self.image_sub = rospy.Subscriber('camera/rgb/image_raw', Image, self.imgCallback)

	def setupSockets(self):
		#Start the receiving socket
		try:
			self.socksend = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			self.socksend.connect((sendAddress,sendPort))
		except socket.error as msg:
			print "Connection failed"
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
		if self.n < 2000:					####### TAKE AWAY
			send_str = self.makeProtoStr(rows,cols,channels,img_str)
			self.send_msg(send_str)
			self.n = self.n+1			#############TAKE AWAY
		
		nparr = np.fromstring(img_str, np.uint8) 		#########Take Away
		dec_img = cv2.imdecode(nparr,1)				########Take Away
		cv2.imshow("Image window", dec_img)			#######Take Away
		cv2.waitKey(3)								########TAKE AWAY

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



rospy.init_node('Sender')
sender = Sender()
while not rospy.is_shutdown():
	time.sleep(0.001)
