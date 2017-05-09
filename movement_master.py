import Receiver
#import Sender
#import Server_Receiver
import Server_Sender
import rospy
import threading
import time
#

class Steering:
	def __init__(self):
		receiver = Receiver.Receiver()
		t1 = threading.Thread(target=receiver.receiveServer, args=())
		#t1.daemon = True
		t1.start()

		self.sender = Server_Sender.SSender(0.5, 0.5)
		sock = self.sender.send_connect("localhost", 8888)
		t2 = threading.Thread(target=self.sender.send_loop, args=([sock]))
		#t2.daemon = True
		t2.start()
		time.sleep(1)
	def setSpeed(self, speed):
		self.sender.setSpeed(speed)
	def setAngle(self, angle):
		self.sender.setAngle(angle)