#include <stdlib.h>

#define BUFFER_LEN 80
#define PORT 5555
#define HOST "127.0.0.1"

#ifdef _WIN32
#define clear_buff(a, b) ZeroMemory(a, b)
#define close_socket(a) closesocket(a)
#undef UNICODE

#define _WIN32_WINNT 0x501
#define WIN32_LEAN_AND_MEAN

#include <windows.h>
#include <ws2tcpip.h>
#include <stdio.h>

#pragma comment (lib, "Ws2_32.lib")
#pragma comment (lib, "Mswsock.lib")
#pragma comment (lib, "AdvApi32.lib")

#else
#define clear_buff(a, b) bzero(a, b)
#define close_socket(a) close(a)

#include <netdb.h>
#include <stdio.h>
#include <string.h>
#include <unistd.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>

#endif

void run_chat(int sockfd) {
    char buff[BUFFER_LEN];

    while (1) {
        clear_buff(buff, sizeof(buff));

        printf("Enter the string: ");
        fgets(buff, BUFFER_LEN, stdin);

        int send_res = send(sockfd, buff, sizeof(buff), 0);
        if (send_res < 0) {
            printf("error, could not send data\n");
            return;
        }

        clear_buff(buff, sizeof(buff));
        int recv_res = recv(sockfd, buff, sizeof(buff), 0);
        if (recv_res < 0) {
            printf("error, could not recv data");
            return;
        }

        printf("From Server : %s", buff);
        if ((strncmp(buff, "exit", 4)) == 0) {
            printf("Client Exit...\n");
            return;
        }
    }
}


struct sockaddr_in getSockAddrIn(int family, char *host, int port) {
    struct sockaddr_in servaddr;

    clear_buff(&servaddr, sizeof(servaddr));
    servaddr.sin_family = family;
    servaddr.sin_addr.s_addr = inet_addr(host);
    servaddr.sin_port = htons(port);

    return servaddr;
}

void run_tcp_cli() {
    #ifdef _WIN32
    WSADATA wsaData;
    if (WSAStartup(MAKEWORD(2,2), &wsaData) != 0) {
        printf("WSAStartup failed with error\n");
        return;
    }
    #endif

    int sock_fd = socket(AF_INET, SOCK_STREAM, 0);
    if (sock_fd == -1) {
        printf("socket creation failed...\n");
        exit(0);
    } else {
        printf("Socket successfully created..\n");
    }

    struct sockaddr_in server_addr = getSockAddrIn(AF_INET, HOST, PORT);
    if (connect(sock_fd, (struct sockaddr *)&server_addr, sizeof(server_addr)) != 0) {
        printf("connection with the server failed...\n");
        exit(0);
    } else {
        printf("connected to the server..\n");
    }

    run_chat(sock_fd);

    shutdown(sock_fd, 1);
    close_socket(sock_fd);

}

int main(int argc, char **argv) {
    run_tcp_cli();
    return 0;
}