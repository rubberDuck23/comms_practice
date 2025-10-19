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

# Let's try this with DOCKER!!!
## Install docker and pull nginx
* sudo apt install docker.io
* docker pull nginx  
* docker pull ubuntu 

# Make your own docker image!!! 
* Create Dockerfile like we have in docker_stuff
* cd to docker_stuff
* docker build -t my_cool_image .    (Maybe instead of just give path to dockder file?)

# Get rid of an image 
* docker rmi -f my_cool_image

# Start a docker container with bash terminal
* docker run -it my_cool_image bash

# View running containers
* docker ps


## Kill a docker container
* docker kill <container_id_or_name>  
* You apprantely have to remove it too with: docker rm <container_id_or_name>


## Copy a file to an activelyh running container
* docker cp <src_path> <container>:<dest_path>

