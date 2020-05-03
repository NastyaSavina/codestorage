#include <stdlib.h>
#include <unistd.h>
#include <stdio.h>

#define BUFFER_LEN 80
#define PORT 5555
#define HOST "127.0.0.1"

#ifdef _WIN32
#define clear_buff(a, b) ZeroMemory(a, b)
#undef UNICODE

#define _WIN32_WINNT 0x501
#define WIN32_LEAN_AND_MEAN

#include <windows.h>
#include <winsock2.h>
#include <ws2tcpip.h>
#include <stdio.h>
#include <winsock.h>

// Need to link with Ws2_32.lib
#pragma comment (lib, "Ws2_32.lib")
#pragma comment (lib, "Mswsock.lib")

#define __POSIX

#else 
#define clear_buff(a, b) bzero(a, b)
#include <string.h>
#include <sys/socket.h>
#include <netinet/in.h>

#endif

void run_chat(int coonection_fd) {
    char buff[BUFFER_LEN];
    
    while(1) {
        clear_buff(&buff, sizeof(buff));

        recv(coonection_fd, buff, sizeof(buff));

        printf("From client: %s\t To client : ", buff);
        clear_buff(&buff, sizeof(buff));

        fgets(buff, BUFFER_LEN, stdin);

        send(coonection_fd, buff, sizeof(buff));

        if (strncmp("exit", buff, 4) == 0) {
            printf("Server Exit...\n");
            break;
        }
    }
}

void run_tcp_server() {
    #ifdef _WIN32
    // Initialize Winsock
    WSADATA wsaData;
    if ((WSAStartup(MAKEWORD(2,2), &wsaData)) != 0) {
        printf("WSAStartup failed with error: %d\n");
        return;
    }
    #endif

    int socket_fd = socket(AF_INET, SOCK_STREAM, 0);
    if (socket_fd == -1) {
        printf("socket creation failed...\n");
        exit(0);
    } else {
        printf("Socket successfully created..\n");
    }

    struct sockaddr_in servaddr;
    clear_buff(&servaddr, sizeof(servaddr));
    servaddr.sin_family = AF_INET;
    servaddr.sin_addr.s_addr = inet_addr(HOST);
    servaddr.sin_port = htons(PORT);

    if ((bind(socket_fd, (struct sockaddr *)&servaddr, sizeof(servaddr))) != 0) {
        printf("socket bind failedtut...\n");
        exit(0);
    } else {
        printf("Socket successfully binded..\n");
    }

    if ((listen(socket_fd, 5)) != 0) {
        printf("Listen failed...\n");
        exit(0);
    } else {
        printf("Server listening..\n");
    }

    int connfd = accept(socket_fd, (struct sockaddr*)NULL, NULL);
    if (connfd < 0) {
        printf("server acccept failed...\n");
        exit(0);
    } else{
        printf("server acccept the client...\n");
    }

    run_chat(connfd);

    shutdown(socket_fd, 1);
    close(socket_fd);
}

int main(void) {

    run_tcp_server();
    return 0;
}