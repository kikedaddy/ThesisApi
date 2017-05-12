import Sender
import Server_Receiver
import threading
import time

class ImageReceiver:
	def __init__(self):
		self.receiver = Server_Receiver.SReceiver()
		t1 = threading.Thread(target=self.receiver.recv_msg_loop, args=([]))
		t1.daemon = True	#Take out daemon
		t1.start()
		sender = Sender.Sender()
		t2 = threading.Thread(target=sender.senderLoop, args=([]))
		t2.daemon = True	#Take out daemon
		t2.start()
		time.sleep(1)
	def getImage(self):
		return self.receiver.getImage()