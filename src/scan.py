import socket
import os 
from dotenv import load_dotenv
load_dotenv()

def is_port_open(ip, port):
    """Check if the port is open on the given IP address."""
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(0.01)  
    try:
        s.connect((ip, port))
    except (socket.timeout, socket.error):
        return False
    else:
        s.close()
        return True

def scan_network_for_open_port(port, ip_range):
    """Scan a range of IP addresses for a specific open port."""
    open_ips = []
    for ip in ip_range:
        if is_port_open(ip, port):
            open_ips.append(ip)
    return open_ips

def generate_ip_range(start_ip, end_ip):
    start = list(map(int, start_ip.split('.')))
    end = list(map(int, end_ip.split('.')))
    temp = start
    ip_range = []
    
    ip_range.append(start_ip)
    while temp != end:
        start[3] += 1
        for i in (3, 2, 1):
            if temp[i] == 256:
                temp[i] = 0
                temp[i-1] += 1
        ip_range.append('.'.join(map(str, temp)))
    
    return ip_range

def get_local_ip_address():
    """Get the local IP address of the machine."""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        ip_address = s.getsockname()[0]
    except Exception as e:
        print(f"Error obtaining IP address: {e}")
        ip_address = None
    finally:
        s.close()
    return ip_address

def calculate_class_c_ip_range(ip_address):
    """Calculate the minimal and maximal IP addresses in a class C subnet."""
    ip_parts = ip_address.split('.')
    ip_parts[-1] = '0'
    min_ip = '.'.join(ip_parts)
    ip_parts[-1] = '255'
    max_ip = '.'.join(ip_parts)
    return min_ip, max_ip

def scan_network():
    """Scan the network for open ports."""
    port_to_scan = int(os.environ.get("PORT"))
    ip = get_local_ip_address()
    min_ip, max_ip = calculate_class_c_ip_range(ip)
    ip_range = generate_ip_range(min_ip, max_ip)
    open_ips = scan_network_for_open_port(port_to_scan, ip_range)
    return open_ips

if __name__ == "__main__":
    scan_network()