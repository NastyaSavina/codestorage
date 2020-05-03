#ifdef _WIN32

#undef _WIN32_WINNT

#else

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>

#define MAX_MESSAGE_LEN 80
#define PORT 8080
#define IP_PROTOCOL 0
#define HOST "192.168.0.103"

#endif

// Function designed for chat between client and server.
void run_chat(int socket_fd) {
    char buff[MAX_MESSAGE_LEN];
    int n;
    // infinite loop for chat
    for (;;) {
        bzero(buff, MAX_MESSAGE_LEN);

        read(socket_fd, buff, sizeof(buff));

        printf("From client: %s\t To client : ", buff);
        bzero(buff, MAX_MESSAGE_LEN);
        n = 0;

        while ((buff[n++] = getchar()) != '\n');

        // and send that buffer to client
        write(socket_fd, buff, sizeof(buff));

        // if msg contains "Exit" then server exit and chat ended.
        if (strncmp("exit", buff, 4) == 0) {
            printf("Server Exit...\n");
            break;
        }
    }
}

int main(int argc, char *argv[]) {
    int socket_fd = socket(AF_INET, SOCK_STREAM, IP_PROTOCOL);
    if (socket_fd == -1) {
        printf("socket creation failed...\n");
        exit(0);
    } else {
        printf("Socket successfully created..\n");
    }

    struct sockaddr_in servaddr;
    bzero(&servaddr, sizeof(servaddr));
    servaddr.sin_family = AF_INET;
    servaddr.sin_addr.s_addr = inet_addr(HOST);
    servaddr.sin_port = htons(PORT);

    if ((bind(socket_fd, (struct sockaddr *)&servaddr, sizeof(servaddr))) != 0) {
        printf("socket bind failed...\n");
        exit(0);
    } else {
        printf("Socket successfully binded..\n");
    }

    // Now server is ready to listen and verification
    if ((listen(socket_fd, 5)) != 0) {
        printf("Listen failed...\n");
        exit(0);
    } else {
        printf("Server listening..\n");
    }

    // Accept the data packet from client and verification
    int connfd = accept(socket_fd, (struct sockaddr*)NULL, NULL);
    if (connfd < 0) {
        printf("server acccept failed...\n");
        exit(0);
    }
    else{
        printf("server acccept the client...\n");}

    // Function for chatting between client and server
    run_chat(connfd);

    // After chatting close the socket
    close(socket_fd);
}

