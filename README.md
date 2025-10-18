# First example in simple_socket_first
This example just does a simple client and server over 127.0.0.1
## Terminal 1
* Do this as root, and output.pcap probably has to be in a directory owned by root
  * tshark -i lo -f "port 65432" -w output.pcap
## Terminal 2
* python3 echo_server.py
## Terminal 3
* python3 echo_client.py