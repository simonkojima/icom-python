import socket
import logging
import threading
import pyicom

        
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

    ip = "127.0.0.1"
    port = 7400
    client = pyicom.client(ip = ip,
                           port = port,
                           length_chunk = 4)

    client.connect()
    print("connection was established")

    while True:
        #input("Press Any Key to Continue")
        data = client.recv()
        print(data)
        client.send(data)
        print("sent")
        #print(data)
    #client.start()

if __name__ == "__main__":
    main()