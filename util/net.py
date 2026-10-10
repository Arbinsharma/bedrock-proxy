import socket

def make_udp_socket(bind_host=None, bind_port=None, timeout=1.0):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.settimeout(timeout)
    if bind_host is not None:
        s.bind((bind_host, bind_port))
    return s

def addr_to_str(addr):
    return f"{addr[0]}:{addr[1]}"
