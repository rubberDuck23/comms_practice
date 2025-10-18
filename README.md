* First example in simple_socket_first
* Do this as root, and output.pcap probably has to be in a directory owned by root
** tshark -i lo -f "port 65432" -w output.pcap
* In another terminal run python3 echo_server.py
* In yet another terminal run python3 echo_client.py