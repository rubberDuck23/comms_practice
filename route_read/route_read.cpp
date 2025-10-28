#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/socket.h>
#include <linux/netlink.h>
#include <linux/rtnetlink.h>
#include <arpa/inet.h>

int NLMSG_GOODSIZE = 30000;

// Helper to convert an IPv4 address from network bytes to a string
void print_ip(unsigned int ip, char *buf) {
    sprintf(buf, "%d.%d.%d.%d",
        (ip >> 0) & 0xFF, (ip >> 8) & 0xFF, (ip >> 16) & 0xFF, (ip >> 24) & 0xFF);
}

int main() {
    int nl_sock;
    struct nlmsghdr *nlh;
    struct rtmsg *rt_msg;
    struct rtattr *rt_attr;
    int len;
    char gateway_ip[INET_ADDRSTRLEN];
    char destination_ip[INET_ADDRSTRLEN];
    char mask_ip[INET_ADDRSTRLEN];

    // Open a Netlink socket
    nl_sock = socket(AF_NETLINK, SOCK_RAW, NETLINK_ROUTE);
    if (nl_sock < 0) {
        perror("Socket Error");
        return 1;
    }

    // Allocate buffer for the Netlink message
    nlh = (struct nlmsghdr *)malloc(NLMSG_GOODSIZE);
    memset(nlh, 0, NLMSG_GOODSIZE);

    // Prepare the Netlink message header
    nlh->nlmsg_len = NLMSG_LENGTH(sizeof(struct rtmsg));
    nlh->nlmsg_type = RTM_GETROUTE;
    nlh->nlmsg_flags = NLM_F_REQUEST | NLM_F_DUMP;

    // Prepare the routing message payload
    rt_msg = (struct rtmsg *)NLMSG_DATA(nlh);
    rt_msg->rtm_family = AF_INET;
    rt_msg->rtm_table = RT_TABLE_MAIN;

    // Send the request
    if (send(nl_sock, nlh, nlh->nlmsg_len, 0) < 0) {
        perror("Send Error");
        close(nl_sock);
        free(nlh);
        return 1;
    }

    printf("%-18s %-18s %-18s\n", "Destination", "Gateway", "Genmask");

    // Read and parse the responses
    len = 0;
    while (1) {
        int bytes_read = recv(nl_sock, nlh, NLMSG_GOODSIZE, 0);
        if (bytes_read < 0) {
            perror("Recv Error");
            break;
        }

        for (; NLMSG_OK(nlh, bytes_read); nlh = NLMSG_NEXT(nlh, bytes_read)) {
            if (nlh->nlmsg_type == NLMSG_DONE) {
                goto cleanup;
            }

            rt_msg = (struct rtmsg *)NLMSG_DATA(nlh);
            if (rt_msg->rtm_family != AF_INET) {
                continue;
            }

            // Initialize storage for route info
            unsigned int dest = 0, gateway = 0;

            // Iterate over attributes to find relevant information
            rt_attr = (struct rtattr *)RTM_RTA(rt_msg);
            int rt_len = RTM_PAYLOAD(nlh);
            for (; RTA_OK(rt_attr, rt_len); rt_attr = RTA_NEXT(rt_attr, rt_len)) {
                if (rt_attr->rta_type == RTA_DST && RTA_PAYLOAD(rt_attr) >= 4) {
                    memcpy(&dest, RTA_DATA(rt_attr), sizeof(dest));
                }
                if (rt_attr->rta_type == RTA_GATEWAY && RTA_PAYLOAD(rt_attr) >= 4) {
                    memcpy(&gateway, RTA_DATA(rt_attr), sizeof(gateway));
                }
            }

            // Print the route entry
            print_ip(dest, destination_ip);
            print_ip(gateway, gateway_ip);
            
            // Calculate and print the netmask from the prefix length
            unsigned int mask_val = (rt_msg->rtm_dst_len == 0) ? 0 : (~0U << (32 - rt_msg->rtm_dst_len));
            print_ip(mask_val, mask_ip);

            printf("%-18s %-18s %-18s\n", destination_ip, gateway_ip, mask_ip);
        }

        

        // Reset the message buffer to prepare for the next read
        memset(nlh, 0, NLMSG_GOODSIZE);
        nlh->nlmsg_len = NLMSG_GOODSIZE;
    }
    

cleanup:
    printf("cleanup time\n");
    close(nl_sock);
    printf("cleanup time 1\n");
    free(nlh);
    printf("cleanup time 2\n");
    return 0;
}