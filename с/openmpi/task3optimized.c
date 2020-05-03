#include <mpi.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

int main(int argc, char **args) {
    MPI_Init(&argc, &args);
    int gridW = 26;
    int gridH = 60;

    int arrW = gridW;
    int arrH = gridH / 2;

    int commSize = 0;
    int myRank = 0;

    MPI_Comm_rank(MPI_COMM_WORLD, &myRank);
    MPI_Comm_size(MPI_COMM_WORLD, &commSize);

    int topProc = myRank == 0 ? MPI_PROC_NULL : myRank - 1;
    int botProc = myRank == commSize - 1 ? MPI_PROC_NULL : myRank + 1;

    double** myArr = (double**)malloc((arrH + 2) * sizeof(double*));

    for (int i = 0; i < arrH + 2; i++) {
        myArr[i] = (double*)malloc(arrW * sizeof(double));
        
        for (int j = 0; j < arrW; j++) {
            myArr[i][j] = 0;
        }
    }

    int borderLine;

    if (myRank == 0) {
        borderLine = 1;
    }

    if (myRank == commSize - 1) {
        borderLine = arrH;
    }

    for (int i = 0; i < arrW; i++) {
        myArr[borderLine][i] = 1;
    }

    for (int i = 1; i < arrH + 1; i++) {
        myArr[i][0] = 1;
        myArr[i][arrW - 1] = 1;
    }

    for (int repeat = 1; repeat < 1000000; repeat++) {
        int sendLine = repeat % 2 == 1 ? arrH : 1;
        int recvLine = repeat % 2 == 1 ? 0 : arrH + 1 ;
        int sendProc = repeat % 2 == 1 ? botProc : topProc;
        int recvProc = repeat % 2 == 1 ? topProc : botProc;
        int start = 0;
        int end = 0;
        
        short isFirstProcess = myRank == 0;
        short isLastProcess = myRank == commSize - 1;
        
        if (isFirstProcess) {
            start = 2 + repeat % 2;
            end = arrH + 1 - repeat % 2;
        } else if (isLastProcess) {
            start = 2 - repeat % 2;
            end = arrH + repeat % 2;
        } else {
            start = 2 - repeat % 2;
            end = arrH + 1 - repeat % 2;
        }

        MPI_Status status;

        MPI_Send(myArr[sendLine], arrW, MPI_DOUBLE, sendProc, 2, MPI_COMM_WORLD);
        MPI_Recv(myArr[recvLine], arrW, MPI_DOUBLE, recvProc, MPI_ANY_TAG, 
                MPI_COMM_WORLD, &status);

        for (int i = start; i < end; i += 2) {
            for (int j = 1; j < arrW-1; j++) {
                myArr[i][j] = (myArr[i-1][j] + myArr[i+1][j] 
                                + myArr[i][j+1] + myArr[i][j-1]) / 4;
            }
        }
    }

    int msec = 1000;
    int stop = 30 * msec;
    usleep(stop * (myRank + 1));

    for (int i = 1; i < arrH + 1; i++) {
        for (int j = 0; j < arrW; j++) {
            printf("%5.2f ", myArr[i][j]);
        }
        printf("\n");
    }

    MPI_Finalize();
}