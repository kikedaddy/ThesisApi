import Server_Sender
import Server_Receiver

HOST = "localhost";
PORT = 8888;
RHOST = "localhost";
RPORT = 8887;

sender = SSender(HOST, PORT);
receiver = SReceiver(RHOST, RPORT, 100);

receiver.connect(RHOST, RPORT, 100);