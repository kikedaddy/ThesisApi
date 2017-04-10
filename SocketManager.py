import socket
import time

def receive (PORT):
	address = ('', PORT)
	server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
	server_socket.bind(address)
	server_socket.settimeout(1)
	recv_data = ""
	print "Listening"
	try:
		recv_data, addr = server_socket.recvfrom(2048)
		print addr,':',recv_data
	except socket.timeout as msg:
		print "No information received"
	server_socket.close()
	return recv_data

def send (PORT, MSG):
	address = ('<broadcast>', PORT)
	client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
	client_socket.connect(address)

	msg = MSG
	#msg = struct.pack('>I', len(msg)) + msg
	client_socket.sendall(msg)

	print "My address: " + str(client_socket.getsockname())
	#client_socket.send(data, address)
	client_socket.close()
