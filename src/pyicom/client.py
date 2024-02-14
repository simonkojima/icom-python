import socket
import logging
import threading

from .common import send, recv

class client():
    def __init__(self,
                 ip,
                 port,
                 name = "icom-client",
                 length_header = 64,
                 length_chunk = 2**12):
        self.ip = ip
        self.port = port
        self.name = name
        self.length_header = length_header
        self.length_chunk = length_chunk
        
        #self.client = None
        self.conn = None
        
    def send(self, data):
        send([self.conn], data, self.length_header, self.length_chunk)
        
    def recv(self):
        data = recv([self.conn], self.length_header, self.length_chunk)
        return data[0]

    def connect(self):
        self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.conn.connect((self.ip, self.port)) 

        #self.send(self.name.encode('utf-8'))
        send([self.conn], self.name.encode('utf-8'), self.length_header, self.length_chunk)
        
def main():
    import sys
    format = '%(asctime)s [%(levelname)s] %(module)s.%(funcName)s %(message)s'
    stdout_handler = logging.StreamHandler(stream = sys.stdout)
    stdout_handler.setFormatter(logging.Formatter(format))
    stdout_handler.setLevel(logging.DEBUG)
    
    root_logger = logging.getLogger(None)
    root_logger.setLevel(logging.DEBUG)
    root_logger.addHandler(stdout_handler)

    ip = socket.gethostbyname(socket.gethostname())
    port = 49153
    client = client(ip = ip,
                         port = port)
    client.connect()
    while True:
        #input("Press Any Key to Continue")
        data = client.recv()
        #print(data)
    #client.start()

if __name__ == "__main__":
    main()