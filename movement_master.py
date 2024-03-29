import Receiver
import Server_Sender
import rospy
import threading
import time
import math
#

class Steering:
	def __init__(self):
		self.receiver = Receiver.Receiver()
		self.t1 = threading.Thread(target=self.receiver.receiveServer, args=())
		#self.t1.daemon = True	#Only needed for attached thread
		self.t1.start()

		self.sender = Server_Sender.SSender()
		self.t2 = threading.Thread(target=self.sender.send_loop, args=([]))
		#self.t2.daemon = True	#Only needed for attached thread
		self.t2.start()
		time.sleep(1)
	def setSpeed(self, speed):
		self.sender.setSpeed(speed)
	#Sets the steering value. Converts the input angle radians to degrees
	def setAngle(self, angle):
		self.sender.setAngle(math.degrees(angle))
	#Aggressive terminate routine
	def terminate(self):
		print self.sender.isRunning()
		self.sender.terminator()
		print self.sender.isRunning()
		self.t1.join(1)
		self.t2.join(1)