import socket
import logging

ICOM_BLOCK = 0
ICOM_NONBLOCK = 1
NONBLOCK_TIMEOUT = 0.01

def send(conn, data, length_header, length_chunk):
    logger = logging.getLogger(__name__)
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

def recv(conn, length_header, length_chunk, mode = ICOM_BLOCK):
    logger = logging.getLogger(__name__)

    if mode == ICOM_NONBLOCK:
        timeout_original = conn.gettimeout()
        conn.settimeout(NONBLOCK_TIMEOUT)
    elif mode == ICOM_BLOCK:
        pass
    else:
        raise ValueError("Unknown mode")
    
    try:
        val = conn.recv(length_header)
    except socket.timeout as e:
        conn.settimeout(timeout_original)
        return b""
        pass
    except Exception as e:
        return b""
        pass

    if mode == ICOM_NONBLOCK:
        conn.settimeout(timeout_original)
    msg_length = int.from_bytes(val, 'little')
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

    return msg
