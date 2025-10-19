import argparse
import socket
import netifaces


# HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
# HOST = "192.168.86.202"
# HOST = "172.17.0.1"

DEFAULT_HOST = netifaces.ifaddresses("docker0")[netifaces.AF_INET][0]['addr']
DEFAULT_PORT = 65432  # Port to listen on (non-privileged ports are > 1023)


def parse_args():

    parser = argparse.ArgumentParser(description="A simple program demonstrating argparse.")

    parser.add_argument(
        "--ip",
        default=DEFAULT_HOST,
        help=f"ip address, default is {DEFAULT_HOST}",
    )

    parser.add_argument(
        "--port",
        type=int,
        default=DEFAULT_PORT,
        help=f"port, default is {DEFAULT_PORT}",
    )


    return parser.parse_args()


def main():

    args = parse_args()

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((args.ip, args.port))
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


if __name__ == "__main__":
    main()