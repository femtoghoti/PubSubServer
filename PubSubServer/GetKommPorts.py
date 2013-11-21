import socket
from PubSubServer.config import MAX_MESSAGE_LENGTH


class GetKommPorts:
    '''demonstration class only
      - coded for clarity, not efficiency
    '''

    def __init__(self, sock=None):
        if sock is None:
            self.sock = socket.socket(
                socket.AF_INET, socket.SOCK_STREAM)
        else:
            self.sock = sock

    def connect(self, host, port):
        self.sock.connect((host, port))

    def mysend(self, msg):
        totalsent = 0
        while totalsent < MAX_MESSAGE_LENGTH:
            sent = self.sock.send(msg[totalsent:])
            if sent == 0:
                raise RuntimeError("socket connection broken")
            totalsent = totalsent + sent

    def myreceive(self):
        msg = ''
        while len(msg) < MAX_MESSAGE_LENGTH:
            chunk = self.sock.recv(MAX_MESSAGE_LENGTH-len(msg))
            if chunk == '':
                return msg
            msg = msg + chunk
        return msg