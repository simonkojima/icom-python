import socket
import logging
import threading
import traceback

try:
    from .common import send, recv 
except:
    from common import send, recv

def excepthook(args):
    print(traceback.format_exc())
    #print(args.exc_value)

class server():
    def __init__(self,
                 ip,
                 port,
                 length_header = 64,
                 length_chunk = 2**12,
                 timeout = 20):
        self.ip = ip
        self.port = port
        self.length_header = length_header
        self.length_chunk = length_chunk
        self.timeout = timeout
        
        self.server = None
        self.conns = list()
        
    def start(self):
        logger = logging.getLogger(__name__)
        
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.settimeout(self.timeout)
        self.server.bind((self.ip, self.port))
        
        print("ICOM server info. ip: %s, port: %s"%(str(self.ip), str(self.port)))
        logger.debug("ICOM server info. ip: %s, port: %s"%(str(self.ip), str(self.port)))
        
        threading.excepthook = excepthook
        thread = threading.Thread(target=self.server_thread, args=(), daemon=True)
        thread.start()
    
    def send(self, data):
        send(self.conns, data, self.length_header, self.length_chunk)
    
    def recv(self):
        return recv(self.conns, self.length_header, self.length_chunk)
    
    def close(self):
        for conn in self.conns:
            conn.close()
        
    def server_thread(self):
        logger = logging.getLogger(__name__)
        while True:
            try:
                self.server.listen()
                conn, addr = self.server.accept()
                #name = recv([conn], self.length_header, self.length_chunk)[0].decode('utf-8')
                self.conns.append(conn)
                logger.debug("New socket connection was established. '%s'"%(str(addr)))
            except Exception as e:
                pass

if __name__ == "__main__":
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
    sv = server(ip = ip,
                    port = port)
    sv.start()
    
    while True:
        try:
            input("Press Any Keys to Continue.")
            data = ""
            for m in range(1000):
                data += "abcdefghijklmnopqrstuvwxyz"
            data += "abcdefgh"
            #print(len(data))
            #server.send(data = "Hello from Server.".encode('utf-8'), names = ['icom-client'])
            sv.send(data = data.encode('utf-8'))
            
            data = sv.recv()
            print("recv: %s"%str(data))

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