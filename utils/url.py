from validators import url, ipv4, ipv6, hostname
import socket

def is_str_url_hname(host: str) -> bool:
    '''
    Check if a given string is an url or an hostname.
    '''
    if url(host) or hostname(host):
        return True

    return False

def is_str_ipv4(host: str) -> bool:
    '''
    Check if a given string is an ipv4 address.
    '''
    return True if ipv4(host) else False

def is_str_ipv6(host: str) -> bool:
    '''
    Check if a given string is an ipv6 address.
    '''
    return True if ipv6(host) else False

def resolve_hostname_ip(host: str) -> str:
    '''
    Get the IP address from an hostname.
    '''
    try:
        host = remove_protocol_url(host.strip())

        addresses = socket.getaddrinfo(host, None)

        ipv4: tuple = []
        ipv6: tuple = []

        for addr in addresses:
            if addr[0] == socket.AF_INET:
                ipv4.append(addr[4][0])
            
            if addr[0] == socket.AF_INET6:
                ipv6.append(addr[4][0])

        return ipv4, ipv6
    
    except socket.gaierror as e:
        print(f"Error retrieving IP address: {e}")
        return [], []

def remove_protocol_url(host: str) -> str:
    '''
    Remove https:// or http:// from the given host.
    '''
    host = host.strip()

    if is_str_url_hname(host):
        return host.replace('http://', '').replace('https://', '')
    
    return host

def check_port(host, port):
    '''
    Get info about an host and a port.
    '''

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(3)

    try:
        sock.connect((host, port))
        print(f"Port {port} on {host} is open.")
        
        local_ip, local_port = sock.getsockname()
        print(f"Connected from local IP {local_ip} and port {local_port}")

    except socket.timeout:
        print(f"Port {port} on {host} is not reachable (connection timed out).")

    except socket.error as e:
        print(f"Port {port} on {host} is closed or unavailable: {e}")

    finally:
        sock.close()

def check_port_2(host, port):
    '''
    Get full info about a particular host and a port.
    '''
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(3)

    try:
        sock.connect((host, port))
        sock.sendall(b"HEAD / HTTP/1.1\r\nHost: " + host.encode() + b"\r\n\r\n")
        
        response = sock.recv(1024).decode()
        print(f"Response from {host}:{port}:\n{response}")

    except socket.timeout:
        print(f"Could not connect to {host}:{port} - connection timed out.")

    except socket.error as e:
        print(f"Could not connect to {host}:{port} - error: {e}")

    finally:
        sock.close()