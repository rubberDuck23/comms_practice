import argparse
import socket

DEFAULT_HOST = "127.0.0.1"  # The server's hostname or IP address
DEFAULT_PORT = 65432  # The port used by the server


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
        s.connect((args.ip, int(args.port)))
        s.sendall(b"Hello, world")
        data = s.recv(1024)

    print(f"Received {data!r}")

if __name__ == "__main__":
    main()