#UDP server responds to broadcast packets
#you can have more than one instance of these running
import socket
import time
import SocketManager

# address = ('', 8886)
# server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
# server_socket.bind(address)


# print "Listening"
# recv_data, addr = server_socket.recvfrom(2048)
# print addr,':',recv_data

# server_socket.close()


# address = ('<broadcast>', 8886)
# client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
# client_socket.connect(address)
# time.sleep(1)
# client_socket.sendto("*"+recv_data, address)

recv_data = SocketManager.receive(8886)
time.sleep(1)
if recv_data:
	SocketManager.send(8886, "fromServer")