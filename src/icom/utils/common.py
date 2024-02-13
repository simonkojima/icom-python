import logging

def send(conns, data, length_header):
    logger = logging.getLogger(__name__)
    for conn in conns:
        conn.send(len(data).to_bytes(length_header, byteorder='little'))
        conn.send(data)

def recv(conns, length_header):
    logger = logging.getLogger(__name__)
    
    data = list()
    for conn in conns:
        msg_length = int.from_bytes(conn.recv(length_header), 'little')
        msg = conn.recv(msg_length).decode('utf-8')
        data.append(msg)
        
    return data
