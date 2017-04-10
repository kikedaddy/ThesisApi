#UDP client broadcasts to server(s)
import socket
from Server_Receiver import SReceiver
from Server_Sender import SSender

SS_address = ('<broadcast>', 8886)
SENDER_PORT = 8887
LISTENING_PORT =8888
MAX_LISTEN = 1
LISTEN_IP = socket.gethostname()
UID = 'kikedaddy'

class Server:
	def __init__(self):
		self.handShake()

	def handShake(self):
		client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
		client_socket.connect(address)

		msg = UID
		client_socket.sendall(msg)

		client_socket.send(data, address)
		found = False
		while not found:
		    recv_data, addr = client_socket.recvfrom(2048)
		    found = True
		    self.addr = addr
		    print addr,recv_data
		senderIp = self.addr[0]
		client_socket.close()


		self.receiver = SReceiver(LISTEN_IP, LISTENING_PORT, MAX_LISTEN)
		self.th = Thread(target=receiver.recv_msg_loop)
		self.th.daemon = True
		self.th.start()
		self.sender = SSender(senderIp, SENDER_PORT)

server = Server()