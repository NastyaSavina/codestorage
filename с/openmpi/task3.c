#include <mpi.h>
#include <stdio.h>
#include <stdlib.h>

double** generateArray(int a, int b) {
    double** arr = (double**)malloc(a * sizeof(double*));

    for (int i = 0; i < a; i++) {
        arr[i] = (double*)malloc(b * sizeof(double));
    }

    for (int i = 0; i < a; i++) {
        for (int j = 0; j < b; j++) {
            arr[i][j] = 0;
        }
    }

    return arr;
};

void print(double **arr, int a, int b) {
    for (int i = 0; i < a; i++) {
        for (int j = 0; j < b; j++) {
            printf("%f ", arr[i][j]);
        }
        printf("\n");
    }
    printf("\n");
}

int main(int argc, char **argv) {
    MPI_Init(&argc, &argv);
    int my_number = 0;
    MPI_Comm_rank(MPI_COMM_WORLD, &my_number);
    int comm_size = 0;
    MPI_Comm_size(MPI_COMM_WORLD, &comm_size);
    int width = 16;
    int block_height = (int)(width / 3);
    int step_count = 2;

    if (my_number == 0) {
        double **arr = generateArray(block_height, width);

        for (int i = 0; i < width; i++) {
            arr[0][i] = 1;
        }
        for (int i = 0; i < block_height; i++) {
            arr[i][0] = 1;
            arr[i][width-1] = 1;
        }

        for (int step = 1; step <= step_count; step++) {
            for (int i = 1 + (step % 2); i < block_height - 1; i += 2) {
                for (int j = 1; j < width - 1; j++) {
                    arr[i][j] = (arr[i - 1][j] + arr[i + 1][j] + arr[i][j + 1] + arr[i][j - 1]) / 4.;
                }
            }

            if (step % 2 == 1) {
                double buff[width];
                MPI_Status status;
                MPI_Recv(buff, width, MPI_DOUBLE, 1, MPI_ANY_TAG, MPI_COMM_WORLD, &status);
                
                for (int j = 1; j < width - 1; j++) {
                    int i = block_height - 1;
                    arr[block_height - 1][j] = (arr[i - 1][j] 
                                                + buff[j] 
                                                + arr[i][j + 1] 
                                                + arr[i][j - 1]) / 4.;
                }
            } else {
                MPI_Send(arr[2], width, MPI_DOUBLE, my_number + 1, 12, MPI_COMM_WORLD);
            }
        }

        print(arr, block_height, width);

    } else if (my_number == comm_size - 1) {
        double **arr = generateArray(block_height, width);
        
        for(int i = 0;i<width; i++) {
            arr[block_height-1][i]=1;
        }
        for (int i = 0; i < block_height; i++) {
            arr[i][width-1] = 1;
            arr[i][0] = 1;
        }


        
        for (int step = 1; step <= step_count; step++) {
            if (step % 2 == 1) {
                double buff[width];
                MPI_Status status;
                MPI_Recv(buff, width, MPI_DOUBLE, my_number-1, MPI_ANY_TAG, MPI_COMM_WORLD, &status);
                
                for (int j = 1; j < width - 1; j++) {
                    int i = 0;
                    arr[i][j] = (buff[j] 
                                                + arr[i + 1][j] 
                                                + arr[i][j + 1] 
                                                + arr[i][j - 1]) / 4.;
                }
            } else {
                MPI_Send(arr[0], width, MPI_DOUBLE, my_number-1, 12, MPI_COMM_WORLD);
            }

            for (int i = 1 + (step % 2); i < block_height - 1; i += 2) {
                for (int j = 1; j < width - 1; j++) {
                    arr[i][j] = (arr[i - 1][j] + arr[i + 1][j] + arr[i][j + 1] + arr[i][j - 1]) / 4.;
                }
            }
        }
        print(arr, block_height, width);


    } else {
        double **arr = generateArray(block_height, width);
        
        for (int i = 0; i < block_height; i++) {
            arr[i][0] = 1;
        }
        for (int i = 0; i < block_height; i++) {
            arr[i][width-1] = 1;
        }

        for (int step = 1; step <= step_count; step++) {

            if (step % 2 == 1) {
                MPI_Send(arr[0], width, MPI_DOUBLE, 0, 12, MPI_COMM_WORLD);
                MPI_Send(arr[block_height - 1], width, MPI_DOUBLE, comm_size - 1, 12, MPI_COMM_WORLD);
                for (int i = (step % 2); i < block_height - 1; i += 2) {
                    for (int j = 1; j < width - 1; j++) {
                        arr[i][j] = (arr[i - 1][j] + arr[i + 1][j] + arr[i][j + 1] + arr[i][j - 1]) / 4.;
                    }
                }
            } else {
                double buff_top[width];
                double buff_bot[width];
                MPI_Status status;
                MPI_Recv(buff_top, width, MPI_DOUBLE, my_number - 1, MPI_ANY_TAG, MPI_COMM_WORLD, &status);
                MPI_Recv(buff_bot, width, MPI_DOUBLE, my_number + 1, MPI_ANY_TAG, MPI_COMM_WORLD, &status);
                int top = 0;
                int bot = block_height - 1;
                for (int j = 1; j < width - 1; j++) {
                    arr[top][j] = (buff_top[j] + arr[top + 1][j] + arr[top][j + 1] + arr[top][j - 1]) / 4.;
                    arr[bot][j] = (arr[bot - 1][j] + buff_bot[j] + arr[bot][j + 1] + arr[bot][j - 1]) / 4.;
                }

                for (int i = (step % 2) + 2; i < block_height - 1; i += 2) {
                    for (int j = 1; j < width - 1; j++) {
                        arr[i][j] = (arr[i - 1][j] + arr[i + 1][j] + arr[i][j + 1] + arr[i][j - 1]) / 4.;
                    }
                }
            }
        }

        print(arr, block_height, width);
    }
    MPI_Finalize();
    return 0;

    // for (int step = 0; step < step_count; step++) {
    //     for (int i = 1 + (step % 2); i < border; i++) {
    //         for (int j = 1; j < border; j++) {
    //             arr[i][j] = (arr[i - 1][j] + arr[i + 1][j] + arr[j][j + 1] + arr[i][j - 1]) / 4.;
    //         }
    //     }
    // }
}