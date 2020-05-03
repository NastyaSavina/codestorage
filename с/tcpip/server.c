#include <sys/socket.h>
#include <netinet/in.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <stdio.h>
#include <time.h>

int main(int argc, char *argv[]) {
    int socket_fd = 0;
    int conn_fd = 0;
    struct sockaddr_in server_addr;


    socket_fd = socket(AF_INET, SOCK_STREAM, 0);
    memset(&server_addr, '0', sizeof(server_addr));

    char sendBuff[1025];
    memset(sendBuff, '0', sizeof(sendBuff));

    server_addr.sin_family = AF_INET;
    server_addr.sin_addr.s_addr = htonl(INADDR_ANY);
    server_addr.sin_port = htons(5000);

    bind(socket_fd, (struct sockaddr*)&server_addr, sizeof(server_addr));
    listen(socket_fd, 10);

    while(1) {
        conn_fd = accept(socket_fd, (struct sockaddr*)NULL, NULL);

        char buff[100] = "some message";
        fputs(buff, stdout);
        write(conn_fd, sendBuff, strlen(sendBuff));

        close(conn_fd);
        sleep(1);
    }
}