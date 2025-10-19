FROM ubuntu:latest


COPY src /root

# Set environment variable for non-interactive apt-get operations
ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \
    apt-get install -y net-tools && \
    apt-get install -y iputils-ping && \
    apt-get install -y vim && \
    apt-get install -y python3 python3-pip