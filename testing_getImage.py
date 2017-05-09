import image_master
import movement_master
import time

#rec = image_master.ImageReceiver()
send = movement_master.Steering()

#print "This is the image"
#print str(rec.getImage())

print "Setting commands"
send.setSpeed(2)
send.setAngle(1)