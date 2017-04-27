import Receiver
import Sender
import rospy
import threading
import time

print "Starting receiver..."

i = 0
image = ''

receiver = Receiver.Receiver()
t1 = threading.Thread(target=receiver.receiveServer, args=())
t1.daemon = True
t1.start()

#receiver.receiveServer()

print "Receiver started..."

print "Rospy initiated..."

t2 = threading.Thread(target=Sender.Sender, args=())
t2.daemon = True
t2.start()

#sender = Sender.Sender()

print "Sender initiated..."

while i < 50:
	time.sleep(0.001)
	if i == 48:
		image = receiver.getImage()
	i += 1
	if i == 49:
		print str(image) + "This is the image we got from calling getImage()"