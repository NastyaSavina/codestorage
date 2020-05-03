#include <mpi.h>
#include <stdio.h>

int main(int argc, char **argv) { 
    MPI_Init(&argc, &argv);
    int myrank = 0;
    MPI_Comm_rank(MPI_COMM_WORLD, &myrank);
    int size = 0;
    MPI_Comm_size(MPI_COMM_WORLD, &size);
    char msg[100];
        printf( "отправил процесс: %d, процессу: %d", myrank, 0);
    if(myrank==size-1)//если процесс последний передает нулевому сообщение, получает от предпоследнего
    {
        char buff[100];
        MPI_Status status;
        snprintf(msg, 100, "отправил процесс: %d, процессу: %d", myrank, 0);
        printf( "отправил процесс: %d, процессу: %d", myrank, 0);
        MPI_Send(msg,100,MPI_CHAR,0,8084,MPI_COMM_WORLD);
        MPI_Recv(buff, 100, MPI_CHAR, myrank-1, status.MPI_TAG, MPI_COMM_WORLD, &status);
    }
    if(myrank==0)//если процесс нулевой ? отправляет первому, получает от последнего процесса
    {
        char buff[100];
        MPI_Status status;
        snprintf(msg, 100, "отправил процесс: %d, процессу: %d", myrank, 0);
        printf( "отправил процесс: %d, процессу: %d", myrank, 0);
        MPI_Send(msg,100,MPI_CHAR,myrank+1,8084,MPI_COMM_WORLD);
        MPI_Recv(buff, 100, MPI_CHAR, size-1, status.MPI_TAG, MPI_COMM_WORLD, &status);
    }
    if(!(myrank==0) && !(myrank==size))// все остальные передают сообщение следуюшему. получают от прошлого
    {
        char buff[100];
        MPI_Status status;
        snprintf(msg, 100, "отправил процесс: %d, процессу: %d", myrank, myrank+1);
        printf( "отправил процесс: %d, процессу: %d", myrank, myrank+1);
        MPI_Send(msg,100,MPI_CHAR,myrank+1,8084,MPI_COMM_WORLD);
        MPI_Recv(buff, 100, MPI_CHAR, myrank, status.MPI_TAG, MPI_COMM_WORLD, &status);   
    }
    MPI_Finalize();
    return 0;
}