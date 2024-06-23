import logging

def send(conns, data, length_header, length_chunk):
    logger = logging.getLogger(__name__)
    for conn in conns:
        conn.send(len(data).to_bytes(length_header, byteorder='little'))
        if len(data) < length_chunk:
            conn.send(data)
        else:
            idx = 0
            while True:
                conn.send(data[idx:(idx + length_chunk)])
                if idx + length_chunk > len(data):
                    break
                idx += length_chunk

def recv(conns, length_header, length_chunk):
    logger = logging.getLogger(__name__)
    data = list()
    for conn in conns:
        msg_length = int.from_bytes(conn.recv(length_header), 'little')
        print(msg_length)
        if msg_length < length_chunk:
            msg = conn.recv(msg_length)
        else:
            length_remained = msg_length
            msg = b""
            while True:
                if length_remained > length_chunk:
                    msg += conn.recv(length_chunk)
                else:
                    msg += conn.recv(length_remained)
                    break
                length_remained -= length_chunk 
        data.append(msg)
    return data
