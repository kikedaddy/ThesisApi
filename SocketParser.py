import socket


def recv_msg(self, sock):
	# Read message length and unpack it into an integer
	raw_msglen = self.recvall(sock, 4)
	if not raw_msglen:
		return None
	msglen = struct.unpack('>I', raw_msglen)[0]
	# Read the message data
	return self.recvall(sock, msglen)

def recvall(self, sock, n):
	# Helper function to recv n bytes or return None if EOF is hit
	data = ''

	while len(data) < n:
		packet = sock.recv(n - len(data))

		if not packet:
			return None
		data += packet
	return data