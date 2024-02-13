import socket
import logging
import threading
import traceback

from utils.common import send, recv 

class icom_server():
    def __init__(self,
                 ip,
                 port,
                 length_header = 64):
        self.ip = ip
        self.port = port
        self.length_header = length_header
        
        self.server = None
        self.conns = dict()
        
    def start(self):
        logger = logging.getLogger(__name__)
        
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self.ip, self.port))
        
        print("ICOM server info. ip: %s, port: %s"%(str(self.ip), str(self.port)))
        
        thread = threading.Thread(target=self.server_thread, args=())
        thread.start()
    
    def send(self, data, names = None):
        if names is None:
            send(list(self.conns.values()), data, self.length_header)
        else:
            conns = list()
            for name in names:
                conns.append(self.conns[name])
            send(conns, data, self.length_header)
    
    def close(self):
        for conn in self.conns:
            conn.close()
        
    def server_thread(self):
        logger = logging.getLogger(__name__)
        while True:
            try:
                self.server.listen()
                conn, addr = self.server.accept()
                msg_length = int.from_bytes(conn.recv(self.length_header), 'little')
                name = conn.recv(msg_length).decode('utf-8')
                self.conns[name] = conn
                logger.debug("New socket connection was established. '%s', Name: %s"%(str(addr), name))
            except KeyboardInterrupt as e:
                self.close()
                print(traceback.format_exc())
                break
            except socket.error as e:
                self.close()
                print(traceback.format_exc())
            except OSError as e:
                self.close()
                print(traceback.format_exc())
            except Exception as e:
                self.close()
                print(traceback.format_exc())
        
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
    server = icom_server(ip = ip,
                         port = port)
    server.start()
    
    while True:
        input("Press Any Keys to Continue.")
        server.send(data = "Hello from Server.".encode('utf-8'), names = ['icom-client'])

if __name__ == "__main__":
    main()