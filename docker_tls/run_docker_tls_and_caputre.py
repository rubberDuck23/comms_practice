from generate_certs import generate_certs


import netifaces

# INTERFACE = "docker0"
INTERFACE = "enp0s3"
HOST = netifaces.ifaddresses(INTERFACE)[netifaces.AF_INET][0]['addr']


def get_server_ip():
    return HOST




def main():

    server_ip = get_server_ip()
    print("server_ip is", server_ip)

    generate_certs(server_ip)

    # Generate certs





if __name__ == "__main__":
    main()