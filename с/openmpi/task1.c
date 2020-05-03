#include <mpi.h>
#include <stdio.h>

int main(int argc, char **argv) { 
    MPI_Init(&argc, &argv);
    int myrank = 0;
    MPI_Comm_rank(MPI_COMM_WORLD, &myrank);
    int size = 0;
    MPI_Comm_size(MPI_COMM_WORLD, &size);
    char msg[100];
    snprintf(msg, 100, "hello from process %d, total %d", myrank, size);
    if (myrank == 0) {
        MPI_Status status;
        char **msgTwo[size];
        for(int i = 0; i < size-1;++i) {
            MPI_Probe(MPI_ANY_SOURCE, MPI_ANY_TAG, MPI_COMM_WORLD, &status);
            int count;
            MPI_Get_count(&status, MPI_CHAR, &count);
            char buff[count];
            MPI_Recv(buff, count, MPI_CHAR, status.MPI_SOURCE, status.MPI_TAG, MPI_COMM_WORLD, &status);
            msgTwo[status.MPI_SOURCE] = buff;
        }
        for (int i = 1; i < size; i++) {
            printf("Message: %s\n", msgTwo[i]);
        }
    } else {
        MPI_Send(msg,100,MPI_CHAR,0,8084,MPI_COMM_WORLD);
    }
    MPI_Finalize();
    return 0;
}