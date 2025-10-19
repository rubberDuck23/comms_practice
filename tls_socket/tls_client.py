import socket
import ssl

import netifaces


# INTERFACE = "docker0"
# HOST = netifaces.ifaddresses(INTERFACE)[netifaces.AF_INET][0]['addr']
HOST = "192.168.86.202"

PORT = 8443
CA_CERTS = '/home/brian/comms_practice/tls_socket/test_ubuntu_new.crt' 

# Create an SSLContext for the client
context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH, cafile=CA_CERTS)

# Create a regular socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    # Wrap the socket with SSL/TLS and connect
    sslsock = context.wrap_socket(sock, server_hostname=HOST)
    sslsock.connect((HOST, PORT))

    sslsock.sendall(b"Hello from secure client!")
    data = sslsock.recv(1024)
    print(f"Received: {data.decode()}")
    sslsock.close()
except ssl.SSLError as e:
    print(f"SSL Error: {e}")
finally:
    sock.close()