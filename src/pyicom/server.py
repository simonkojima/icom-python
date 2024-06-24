import socket
import logging
import threading
import traceback

try:
    from .common import send, recv, ICOM_BLOCK, ICOM_NONBLOCK
except:
    from common import send, recv, ICOM_BLOCK, ICOM_NONBLOCK

def excepthook(args):
    print(traceback.format_exc())
    #print(args.exc_value)

class server():
    def __init__(self,
                 ip,
                 port,
                 length_header = 64,
                 length_chunk = 4096,
                 timeout = 20):
        self.ip = ip
        self.port = port
        self.length_header = length_header
        self.length_chunk = length_chunk
        self.timeout = timeout
        
        self.server = None
        self.conn = None
        
    def start(self):
        logger = logging.getLogger(__name__)
        
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.settimeout(self.timeout)
        self.server.bind((self.ip, self.port))
        self.server.listen()
        
        print("ICOM server info. ip: %s, port: %s"%(str(self.ip), str(self.port)))
        logger.debug("ICOM server info. ip: %s, port: %s"%(str(self.ip), str(self.port)))
    
    def send(self, data):
        send(self.conn, data, self.length_header, self.length_chunk)
    
    def recv(self):
        return recv(self.conn, self.length_header, self.length_chunk, ICOM_BLOCK)

    def recv_nonblock(self):
        return recv(self.conn, self.length_header, self.length_chunk, ICOM_NONBLOCK)
    
    def close(self):
        self.conn.close()
        
    def wait_for_connection(self):
        logger = logging.getLogger(__name__)
        logger.debug("waiting for connection...")
        conn, addr = self.server.accept()
        conn.settimeout(self.timeout)
        self.conn = conn
        logger.debug("New socket connection was established. '%s'"%(str(addr)))

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
    sv = server(ip = ip,
                port = port,
                length_header = 64,
                length_chunk = 4096)
    sv.start()
    sv.wait_for_connection()

    import time
    
    while True:
        try:
            data = "abcdefghijklmnopqrstuvwxyz"
            sv.send(data = data.encode('utf-8'))
            logger.debug("Sent: %s"%str(data))
            
            while 1:
                data = sv.recv_nonblock()
                if (len(data) != 0):
                    break
            print("nonblock Received: %s"%str(data))

            data = "abcdefghijklmnopqrstuvwxyz"
            sv.send(data = data.encode('utf-8'))
            logger.debug("Sent: %s"%str(data))
            
            data = sv.recv()
            print("block Received: %s"%str(data))

        except KeyboardInterrupt as e:
            sv.close()
            print(e)
            print(traceback.format_exc())
            break
        except Exception as e:
            sv.close()
            print(e)
            print(traceback.format_exc())
            break