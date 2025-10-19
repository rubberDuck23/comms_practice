import netifaces
import subprocess
import time

INTERFACE = "docker0"
IP = netifaces.ifaddresses(INTERFACE)[netifaces.AF_INET][0]['addr']
PORT = "65430"
IMAGE_NAME = "mega_image"
OUTPUT_FILE = "/root/out.pcap"

def main():
    
    tshark_process = subprocess.Popen(["tshark", "-i", INTERFACE, "-f", f"port {PORT}", "-w", f"{OUTPUT_FILE}"])
    server_process = subprocess.Popen(["python3", "docker_echo_server.py", "--port", PORT, "--ip", IP])

    time.sleep(1)

    subprocess.call(f"docker run {IMAGE_NAME} python3 /root/echo_client.py --ip {IP} --port {PORT}", shell=True)

    
    time.sleep(1)

    # Terminate the subprocess gracefully
    tshark_process.terminate()
    server_process.terminate()
    server_process.wait()
    tshark_process.wait() 


if __name__ == "__main__":
    main()