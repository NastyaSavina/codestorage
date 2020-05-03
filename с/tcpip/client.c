#include <sys/socket.h>
#include <netinet/in.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <unistd.h>
#include <arpa/inet.h>

int main(int argc, char *argv[]) {
    int socket_fd = 0;
    int read_bytes_count = 0;
    char recvBuff[1024];
    struct sockaddr_in server_addr;

    if(argc != 2) {
        printf("\n Usage: %s <ip of server> \n",argv[0]);
        return 1;
    }

    memset(recvBuff, '0',sizeof(recvBuff));
    if((socket_fd = socket(AF_INET, SOCK_STREAM, 0)) < 0)
    {
        printf("\n Error : Could not create socket \n");
        return 1;
    }

    memset(&server_addr, '0', sizeof(server_addr));

    server_addr.sin_family = AF_INET;
    server_addr.sin_port = htons(5000);

    if(inet_pton(AF_INET, argv[1], &server_addr.sin_addr) <= 0)
    {
        printf("\n inet_pton error occured\n");
        return 1;
    }

    if(connect(socket_fd, (struct sockaddr *)&server_addr, sizeof(server_addr)) < 0)
    {
        printf("\n Error : Connect Failed \n");
        return 1;
    }

    while ((read_bytes_count = read(socket_fd, recvBuff, sizeof(recvBuff) - 1)) > 0)
    {
        recvBuff[read_bytes_count] = 0;
        char print_buff[100] = "buffer to write\n";
        fputs(print_buff, stdout);

        if(fputs(recvBuff, stdout) == EOF)
        {
            printf("\n Error : Fputs error\n");
        }
    }

    if(read_bytes_count < 0)
    {
        printf("\n Read error \n");
    }

    return 0;
}