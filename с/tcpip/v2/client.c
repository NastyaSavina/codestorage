#include <netdb.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>

#define MAX_MESSAGE_LEN 80
#define PORT 8080
#define LOCALHOST "192.168.0.103"
#define SA struct sockaddr

void run_chat(int sockfd) {
    char buff[MAX_MESSAGE_LEN];
    int n;
    int exit = 0;

    while (!exit) {
        bzero(buff, sizeof(buff));
        printf("Enter the string: ");
        n = 0;
        while ((buff[n++] = (char) getchar()) != '\n');
        write(sockfd, buff, sizeof(buff));
        bzero(buff, sizeof(buff));
        read(sockfd, buff, sizeof(buff));
        printf("From Server : %s", buff);
        if ((strncmp(buff, "exit", 4)) == 0) {
            printf("Client Exit...\n");
            exit = 1;
        }
    }
}

struct sockaddr_in getSockAddrIn(int family, char *host, int port) {
    struct sockaddr_in servaddr;
    bzero(&servaddr, sizeof(servaddr));
    servaddr.sin_family = family;
    servaddr.sin_addr.s_addr = inet_addr(host);
    servaddr.sin_port = htons(port);

    return servaddr;
}

int main() {
    int sock_fd;

    sock_fd = socket(AF_INET, SOCK_STREAM, 0);
    if (sock_fd == -1) {
        printf("socket creation failed...\n");
        exit(0);
    } else {
        printf("Socket successfully created..\n");
    }

    struct sockaddr_in server_addr = getSockAddrIn(AF_INET, LOCALHOST, PORT);
    if (connect(sock_fd, (struct sockaddr *) &server_addr, sizeof(server_addr)) != 0) {
        printf("connection with the server failed...\n");
        exit(0);
    } else {
        printf("connected to the server..\n");
    }

    run_chat(sock_fd);

    close(sock_fd);
}

