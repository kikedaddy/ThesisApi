#UDP client broadcasts to server(s)
import socket

address = ('<broadcast>', 8886)
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
client_socket.connect(address)

msg = "Request"
msg = struct.pack('>I', len(msg)) + msg
client_socket.sendall(msg)

client_socket.send(data, address)
while True:
    recv_data, addr = client_socket.recvfrom(2048)
    print addr,recv_data