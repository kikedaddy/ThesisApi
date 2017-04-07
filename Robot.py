from Receiver import Receiver
from Sender import Sender
#import SocketParser
import socket
import threading

HS_ADRESS = ('', 8886)
SENDER_PORT = 8888
LISTENING_PORT =8887
MAX_LISTEN = 1
LISTEN_IP = socket.gethostname()
UID = 'kikedaddy'

class Robot:
	def __init__(self):
		self.handShake()
	
	def handShake (self):


		server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
		server_socket.bind(HS_ADRESS)

		found = False
		while not found:
			print "Listening"
			recv_data, addr = server_socket.recvfrom(2048)
			print addr,':',recv_data
			if recv_data==UID:
				found = True
				self.addr = addr
		senderIp = self.addr[0]
		server_socket.close()

		self.receiver = Receiver(LISTEN_IP, LISTENING_PORT, MAX_LISTEN)
		self.th = Thread(target=receiver.receiveServer)
		self.th.daemon = True
		self.th.start()
		self.sender = Sender(senderIp, SENDER_PORT)


robot = Robot()