import socket
import logging

try:
    from .common import send, recv, ICOM_BLOCK, ICOM_NONBLOCK
except:
    from common import send, recv, ICOM_BLOCK, ICOM_NONBLOCK

class client():
    def __init__(self,
                 ip,
                 port,
                 length_header = 64,
                 length_chunk = 4096):
        self.ip = ip
        self.port = port
        self.length_header = length_header
        self.length_chunk = length_chunk
        
        #self.client = None
        self.conn = None
        
    def send(self, data):
        send(self.conn, data, self.length_header, self.length_chunk)
        
    def recv(self):
        data = recv(self.conn, self.length_header, self.length_chunk, ICOM_BLOCK)
        return data
    
    def recv_nonblock(self):
        data = recv(self.conn, self.length_header, self.length_chunk, ICOM_NONBLOCK)
        return data

    def connect(self):
        logger = logging.getLogger(__name__)
        logger.debug("Connecting to ip: %s, port: %s"%(str(self.ip), str(self.port)))
        self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.conn.connect((self.ip, self.port)) 
        logger.debug("Connected to ip: %s, port: %s"%(str(self.ip), str(self.port)))

if __name__ == "__main__":
    import sys
    format = '%(asctime)s [%(levelname)s] %(module)s.%(funcName)s %(message)s'
    stdout_handler = logging.StreamHandler(stream = sys.stdout)
    stdout_handler.setFormatter(logging.Formatter(format))
    stdout_handler.setLevel(logging.DEBUG)
    
    root_logger = logging.getLogger(None)
    root_logger.setLevel(logging.DEBUG)
    root_logger.addHandler(stdout_handler)
    
    logger = logging.getLogger(__name__)

    ip = socket.gethostbyname(socket.gethostname())
    port = 49153
    client = client(ip = ip,
                    port = port,
                    length_header = 64,
                    length_chunk = 4096)
    client.connect()

    import time
    while True:
        data = client.recv()
        logger.debug("Received: %s"%str(data))
        time.sleep(3)

        client.send(data)
        logger.debug("Sent: %s"%str(data))
        time.sleep(1)
        #print(data)
    #client.start()