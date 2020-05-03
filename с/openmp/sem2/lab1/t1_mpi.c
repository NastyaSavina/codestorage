#include <mpi.h>
#include <stdio.h>
#include <stdlib.h>
#include <math.h>

#define A_ARR_TAG 1
#define B_ARR_TAG 2

void recv_b_data(double **b_arr, int recv_from, int n, int p) {
    MPI_Status b_status;
    double *b_buffer = malloc(sizeof(double) * (n * p));
    MPI_Recv(b_buffer, n * p, MPI_DOUBLE, recv_from, B_ARR_TAG, MPI_COMM_WORLD, &b_status);
    for (int i = 0; i < n * p; i++) {
        b_arr[(int)(ceil(i / p))][(int)(i % p)] = b_buffer[i];
    }
}

void recv_a_data(double **a_arr, int recv_from, int n, int p) {
    MPI_Status a_status;
    double *a_buffer = malloc(sizeof(double) * (n * p));
    MPI_Recv(a_buffer, n * p, MPI_DOUBLE, recv_from, A_ARR_TAG, MPI_COMM_WORLD, &a_status);
    for (int i = 0; i < n * p; i++) {
        a_arr[(int)(ceil(i / n))][(int)(i % n)] = a_buffer[i];
    }
}


void init_process(double **a_arr, double **b_arr, int n, int p) {
    recv_a_data(a_arr, 0, n, p);
    recv_b_data(b_arr, 0, n, p);
}


void send_b_data(double **b_arr, int send_to, int n, int p) {
    double *buffer = malloc(sizeof(double) * n * p);
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < p; j++) {
            buffer[i * p + j] = b_arr[i][j];
        }
    }
    MPI_Send(buffer, n * p, MPI_DOUBLE, send_to, B_ARR_TAG, MPI_COMM_WORLD);
}


double mult(double a_line[], double b_line[], int n) {
    double res = 0;

    for (size_t i = 0; i < n; i++) {
        res += a_line[i] * b_line[i];
    }
    
    return res;
};

double** flat_map(double **arr, int a, int b) {
    double *buffer = malloc(sizeof(double) * a * b);

    
}

int main(int argc, char **argv) { 
    MPI_Init(&argc, &argv);
    int myrank = 0;
    MPI_Comm_rank(MPI_COMM_WORLD, &myrank);
    int size = 0;
    MPI_Comm_size(MPI_COMM_WORLD, &size);

    int n = 4;
    int p = 2;
    int parts_count = 2;
    
    if (myrank == 0) {
        double a_arr[n][n];
        double b_arr[n][n];
        double result_array[n][n];

        for (int i = 0; i < n; i++) {
            for (int j = 0; j < n; j++) {
                a_arr[i][j] = (i + 1) * (j + 1);
                b_arr[i][j] = (i + 1) * (j + 1);
            }
        }

        double *buffer = malloc(sizeof(double) * n * p);
        for (int part = 0; part < parts_count; part++) {
            for (int i = 0; i < p; i++) {
                for (int j = 0; j < n; j++) {
                    buffer[i * n + j] = a_arr[i + part * p][j];
                }
            }
            MPI_Send(buffer, n * p, MPI_DOUBLE, part + 1, A_ARR_TAG, MPI_COMM_WORLD);

            for (int i = 0; i < n; i++) {
                for (int j = 0; j < p; j++) {
                    buffer[i * p + j] = a_arr[i][j + part * p];
                }
            }
            MPI_Send(buffer, n * p, MPI_DOUBLE, part + 1, B_ARR_TAG, MPI_COMM_WORLD);
        }

        int i_start;
        int j_start;
        MPI_Status status;
        double *res_buffer;
        
        for (int i = 0; i < parts_count * parts_count; i++) {
            res_buffer = malloc(sizeof(double) * p * p);
            MPI_Recv(res_buffer, p * p, MPI_DOUBLE, MPI_ANY_SOURCE, MPI_ANY_TAG, MPI_COMM_WORLD, &status);

            i_start = (int)(ceil((status.MPI_TAG - 1) / parts_count)) * p;
            j_start = (int)((status.MPI_TAG - 1) % parts_count) * p;

            printf("tag: %d, i_start: %d, j_start: %d \n", status.MPI_TAG, i_start, j_start);

            for (int i = i_start; i < i_start + p; i++) {
                for (int j = j_start; j < j_start + p; j++) {
                    result_array[i][j] = res_buffer[(i - i_start) * p + (j - j_start)];
                }
            }
        }


        for (int i = 0; i < n; i++) {
            for (int j = 0; j < n; j++) {
                printf("\t%.f", result_array[i][j]);
            }
            printf("\n");
        }
        
    } else {
        double **a_rows = malloc(sizeof(double*) * p);
        double **b_cols = malloc(sizeof(double*) * n);
        double res_arr[p][p];
        int res_i_part_num = myrank;
        int res_j_part_num = myrank;
        int result_sector_index = (myrank - 1) * parts_count + myrank;

        for (int i = 0; i < n; i++) {
            a_rows[i] = malloc(sizeof(double) * n);
            b_cols[i] = malloc(sizeof(double) * p);
        }

        init_process(a_rows, b_cols, n, p);

        for (int step = 0; step < parts_count; step++) {

            for (int i = 0; i < p; i++) {
                for (int j = 0; j < p; j++) {
                    double a_row[n];
                    double b_col[n];
                    
                    for (int k = 0; k < n; k++) {
                        a_row[k] = a_rows[i][k];
                        b_col[k] = b_cols[k][j];
                    }   

                    res_arr[i][j] = mult(a_row, b_col, n);
                }
            }

            double *res_arr_buffer = malloc(sizeof(double) * p * p);
            for (int i = 0; i < p; i++) {
                for (int j = 0; j < p; j++) {
                    res_arr_buffer[i * p + j] = res_arr[i][j];
                }
            }

            int send_to = myrank == 1 ? parts_count : myrank - 1;
            send_b_data(b_cols, send_to, n, p);
            MPI_Send(res_arr_buffer, p * p, MPI_DOUBLE, 0, result_sector_index, MPI_COMM_WORLD);

            int recv_from = myrank == parts_count ? 1 : myrank + 1;
            recv_b_data(b_cols, recv_from, n, p);


            if (result_sector_index % parts_count == 0) {
                result_sector_index = result_sector_index - parts_count;
            }
            result_sector_index += 1;
        }
    }

    MPI_Finalize();
    return 0;
}