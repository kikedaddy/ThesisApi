#UDP client broadcasts to server(s)
import socket
import SocketManager

# address = ('<broadcast>', 8886)
# client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
# client_socket.connect(address)

# msg = "Request"
# #msg = struct.pack('>I', len(msg)) + msg
# client_socket.sendall(msg)

# print "My address: " + str(client_socket.getsockname())
# #client_socket.send(data, address)
# client_socket.close()


# address = ('', 8886)
# server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
# server_socket.bind(address)

# recv_data, addr = server_socket.recvfrom(2048)
# print addr,recv_data

SocketManager.send(8886,"Fromclient")

SocketManager.receive(8886)