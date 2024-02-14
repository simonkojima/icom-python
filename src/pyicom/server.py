import socket
import logging
import threading
import traceback

from .common import send, recv 

def excepthook(args):
    print(args.exc_value)

class server():
    def __init__(self,
                 ip,
                 port,
                 length_header = 64,
                 length_chunk = 2**12):
        self.ip = ip
        self.port = port
        self.length_header = length_header
        self.length_chunk = length_chunk
        
        self.server = None
        self.conns = dict()
        
    def start(self):
        logger = logging.getLogger(__name__)
        
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #self.server.settimeout(0.1)
        self.server.bind((self.ip, self.port))
        
        print("ICOM server info. ip: %s, port: %s"%(str(self.ip), str(self.port)))
        logger.debug("ICOM server info. ip: %s, port: %s"%(str(self.ip), str(self.port)))
        
        threading.excepthook = excepthook
        thread = threading.Thread(target=self.server_thread, args=(), daemon=True)
        thread.start()
    
    def send(self, data, names = None):
        if names is None:
            send(list(self.conns.values()), data, self.length_header, self.length_chunk)
        else:
            conns = list()
            for name in names:
                conns.append(self.conns[name])
            send(conns, data, self.length_header, self.length_chunk)
    
    def recv(self, names = None):
        if names is None:
            data = recv(list(self.conns.values()), self.length_header, self.length_chunk)
        else:
            conns = list()
            for name in names:
                conns.append(self.conns[name])
            data = recv(conns, self.length_header, self.length_chunk)
        
        return data
    
    def close(self):
        for conn in list(self.conns.values()):
            conn.close()
        
    def server_thread(self):
        logger = logging.getLogger(__name__)
        while True:
            self.server.listen()
            conn, addr = self.server.accept()
            name = recv([conn], self.length_header, self.length_chunk)[0].decode('utf-8')
            self.conns[name] = conn
            logger.debug("New socket connection was established. '%s', Name: %s"%(str(addr), name))
        
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
    server = server(ip = ip,
                         port = port)
    server.start()
    
    while True:
        try:
            input("Press Any Keys to Continue.")
            data = ""
            for m in range(1000):
                data += "abcdefghijklmnopqrstuvwxyz"
            data += "abcdefgh"
            print(len(data))
            #server.send(data = "Hello from Server.".encode('utf-8'), names = ['icom-client'])
            server.send(data = data.encode('utf-8'), names=['icom-client'])
        except KeyboardInterrupt as e:
            server.close()
            print(traceback.format_exc())
            break
        except Exception as e:
            server.close()
            print(traceback.format_exc())
            break

if __name__ == "__main__":
    main()