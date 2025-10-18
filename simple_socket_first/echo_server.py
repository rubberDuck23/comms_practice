import socket

HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
# HOST = "192.168.86.202"
PORT = 65432  # Port to listen on (non-privileged ports are > 1023)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        print(f"Connected by {addr}")
        while True:
            data = conn.recv(1024)
            print("server recieved data:", data)
            if not data:
                break
            print("sending data")
            conn.sendall(data + b" extra server message part")
            print("data sent")

print("exiting echo server")
