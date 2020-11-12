def get_ip():
    import socket
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    return local_ip

def parse_ip(ip_address):
    ip_bytes = ip_address.split('.')
    for i in range(len(ip_bytes)):
        ip_bytes[i] = int(ip_bytes[i])

    return ip_bytes


def send_data(ip_address, port, data):
    import socket
    sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
    sock.sendto(data, (ip_address, port))
