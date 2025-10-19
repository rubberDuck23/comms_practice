import socket
import ssl

import netifaces


# INTERFACE = "docker0"
# HOST = netifaces.ifaddresses(INTERFACE)[netifaces.AF_INET][0]['addr']
HOST = "192.168.86.202"


PORT = 8443
CERTFILE = '/home/brian/comms_practice/tls_socket/test_ubuntu_new.crt'  # Path to server certificate
KEYFILE = '/home/brian/comms_practice/tls_socket/test_ubuntu_new.key'    # Path to server private key

# Create an SSLContext
context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
context.load_cert_chain(certfile=CERTFILE, keyfile=KEYFILE)

# Create a regular socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((HOST, PORT))
sock.listen(5)

print(f"Listening on {HOST}:{PORT}")

while True:
    conn, addr = sock.accept()
    print(f"Connection from {addr}")
    try:
        # Wrap the socket with SSL/TLS
        sslsock = context.wrap_socket(conn, server_side=True)
        data = sslsock.recv(1024)
        print(f"Received: {data.decode()}")
        sslsock.sendall(b"Hello from secure server!")
        sslsock.close()
    except ssl.SSLError as e:
        print(f"SSL Error: {e}")
    finally:
        conn.close()