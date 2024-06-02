import socket
import os 
from dotenv import load_dotenv
load_dotenv()

def is_port_open(ip, port):
    """Check if the port is open on the given IP address."""
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(0.1)  
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
            print(f"Port {port} is open on {ip}")
    return open_ips

""" Define the range of IPs to scan (example: 192.168.1.0 to 192.168.1.255) """

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

if __name__ == "__main__":
    
    port_to_scan = int(os.environ.get("PORT"))
    start_ip = "192.168.1.0"
    end_ip = "192.168.1.255"
    
    ip_range = generate_ip_range(start_ip, end_ip)
    open_ips = scan_network_for_open_port(port_to_scan, ip_range)
    
    if open_ips:
        print(f"Machines with port {port_to_scan} open: {open_ips}")
    else:
        print(f"No machines found with port {port_to_scan} open in the given range.")
