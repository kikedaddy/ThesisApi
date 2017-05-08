import Receiver
#import Sender
#import Server_Receiver
import Server_Sender
import rospy
import threading
import time

print "Starting receiver..."

i = 0
speed = ''
angle = ''

receiver = Receiver.Receiver()
t1 = threading.Thread(target=receiver.receiveServer, args=())
t1.daemon = True
t1.start()

#receiver.receiveServer()

print "Receiver started..."

print "Rospy initiated..."

sender = Server_Sender.SSender(0.5, 0.5)
sock = sender.send_connect("localhost", 8888)

t2 = threading.Thread(target=sender.send_loop, args=([sock]))
t2.daemon = True
t2.start()

#sender = Sender.Sender()

print "Sender initiated..."

while i < 4500:
	time.sleep(0.001)
	if i == 1000:
		sender.setSpeed(2)
		sender.setAngle(3)

		print str(receiver.getSpeed()) + ", " + str(receiver.getAngle())
	if i == 4490:
		print "And now: " + str(receiver.getSpeed()) + ", " + str(receiver.getAngle())
	i += 1