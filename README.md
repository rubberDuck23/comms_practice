# First example in simple_socket_first
This example just does a simple client and server over 127.0.0.1
This generates TCP traffic where data is unecrypted and can be read
Can run on different VMs by changing the address on python file from 127.0.0.1 to whatever the ip of the server is

## Terminal 1
* tshark -i lo -f "port 65432" -w output.pcap
  * Do this as root, and output.pcap probably has to be in a directory owned by root
  * I got interface of "lo" by running ip addr
  * If going across two VMS, I chagned "lo" to "enp0s3"
## Terminal 2
* python3 echo_server.py
## Terminal 3
* python3 echo_client.py