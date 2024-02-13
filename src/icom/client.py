import socket
import logging
import threading

from utils.common import send, recv

class icom_client():
    def __init__(self,
                 ip,
                 port,
                 name = "icom-client",
                 length_header = 64):
        self.ip = ip
        self.port = port
        self.name = name
        self.length_header = length_header
        
        #self.client = None
        self.conn = None
        
    def send(self, data):
        send([self.conn], data, self.length_header)
        
    def recv(self):
        data = recv([self.conn], self.length_header)
        return data[0]

    def connect(self):
        self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.conn.connect((self.ip, self.port)) 

        self.send(self.name.encode('utf-8'))
        
def main():
    ip = socket.gethostbyname(socket.gethostname())
    port = 49153
    client = icom_client(ip = ip,
                         port = port)
    client.connect()
    while True:
        input("Press Any Key to Continue")
        data = client.recv()
        print(data)
    #client.start()

if __name__ == "__main__":
    main()