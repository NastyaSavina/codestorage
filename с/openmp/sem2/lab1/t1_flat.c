#include <mpi.h>
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <time.h>
#include <unistd.h>
#include <sys/stat.h>

#define A_ARR_TAG 1
#define B_ARR_TAG 2
#define LEN 50

void get_formatted_time(char *curr_date);
char* get_filepath(char *dir, int tid);
char* get_log_dir(char *root_path);
FILE* get_log_file(char *log_dir, int rank);
void send_data(double **arr, int send_to, int n, int p, int send_tag);
void recv_data(double **arr, int recv_from, int n, int p, int recv_tag);
void init_process(double **a_arr, double **b_arr, int n, int p);
double mult(double a_line[], double b_line[], int n);
void write_arr_to_file(FILE *file, char *message, double **arr, int n, int p);


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
        char *dir = get_log_dir("/Users/me/programs/с/openmp/sem2/lab1/");
        FILE *f = get_log_file(dir, myrank);
        double **a_arr = malloc(sizeof(double*) * n);
        double **b_arr = malloc(sizeof(double*) * n);
        double **result_array = malloc(sizeof(double*) * n);

        for (int i = 0; i < n; i++) {
            a_arr[i] = malloc(sizeof(double) * n);
            b_arr[i] = malloc(sizeof(double) * n);
            result_array[i] = malloc(sizeof(double) * n);
            for (int j = 0; j < n; j++) {
                a_arr[i][j] = (i + 1) * (j + 1);
                b_arr[i][j] = (i + 1) * (j + 1);
                result_array[i][j] = 0;
            }
        }

        write_arr_to_file(f, "init a_arr:", a_arr, n, n);
        write_arr_to_file(f, "init b_arr:", b_arr, n, n);

        double *buffer = malloc(sizeof(double) * n * p);
        for (int part = 0; part < parts_count; part++) {
            for (int i = 0; i < p; i++) {
                for (int j = 0; j < n; j++) {
                    buffer[i * n + j] = a_arr[i + part * p][j];
                }
            }
            MPI_Send(buffer, n * p, MPI_DOUBLE, part + 1, A_ARR_TAG, MPI_COMM_WORLD);

            for (int i = 0; i < p; i++) {
                for (int j = 0; j < n; j++) {
                    buffer[i * n + j] = a_arr[j][i + part * p];
                }
            }
            MPI_Send(buffer, n * p, MPI_DOUBLE, part + 1, B_ARR_TAG, MPI_COMM_WORLD);
            fclose(f);
        }

        int i_start;
        int j_start;
        MPI_Status status;
        double *res_buffer = malloc(sizeof(double) * p * p);
        
        for (int i = 0; i < parts_count * parts_count; i++) {
            MPI_Recv(res_buffer, p * p, MPI_DOUBLE, MPI_ANY_SOURCE, MPI_ANY_TAG, MPI_COMM_WORLD, &status);

            i_start = (int)(ceil((status.MPI_TAG - 1) / parts_count)) * p;
            j_start = (int)((status.MPI_TAG - 1) % parts_count) * p;

            for (int i = i_start; i < i_start + p; i++) {
                for (int j = j_start; j < j_start + p; j++) {
                    result_array[i][j] = res_buffer[(i - i_start) * p + (j - j_start)];
                }
            }
        }
        
        write_arr_to_file(f, "result_arr: ", result_array, n, n);
    } else {
        char *dir = get_log_dir("/Users/me/programs/с/openmp/sem2/lab1/");
        FILE *f = get_log_file(dir, myrank);
        double **a_rows = malloc(sizeof(double*) * p);
        double **b_cols = malloc(sizeof(double*) * p);
        double **res_arr = malloc(sizeof(double*) * p);

        int res_sector = (myrank - 1) * parts_count + myrank;

        for (int i = 0; i < p; i++) {
            a_rows[i] = malloc(sizeof(double) * n);
            b_cols[i] = malloc(sizeof(double) * n);
            res_arr[i] = malloc(sizeof(double) * p);
        }

        init_process(a_rows, b_cols, n, p);

        for (int step = 0; step < parts_count; step++) {
            char *message = malloc(sizeof(char) * 100);
            fprintf(f, "\n\n\nArrays for %d sector calculation:\n", res_sector);
            write_arr_to_file(f, "a_rows: ", a_rows, p, n);
            write_arr_to_file(f, "b_arr: ", b_cols, p, n);

            for (int i = 0; i < p; i++) {
                for (int j = 0; j < p; j++) {
                    res_arr[i][j] = mult(a_rows[i], b_cols[j], n);
                }
            }

            fprintf(f, "sector %d calculation result:\n", res_sector);
            write_arr_to_file(f, "res_arr: ", res_arr, p, p);

            int send_to = myrank == 1 ? parts_count : myrank - 1;
            send_data(b_cols, send_to, n, p, B_ARR_TAG);

            int recv_from = myrank == parts_count ? 1 : myrank + 1;
            recv_data(b_cols, recv_from, n, p, B_ARR_TAG);

            send_data(res_arr, 0, p, p, res_sector);
            if (res_sector % parts_count == 0) {
                res_sector = res_sector - parts_count;
            }
            res_sector += 1;
        }
        fclose(f);
    }

    MPI_Finalize();
    return 0;
}


void get_formatted_time(char *curr_date){
   char buf[LEN];
   time_t curtime;
   struct tm *loc_time; 
   curtime = time (NULL);
   loc_time = localtime (&curtime);
   strftime(curr_date, LEN, "%Y-%m-%dT%H:%M:%S", loc_time);
}


char* get_filepath(char *dir, int tid) {
    char id[10];
    snprintf(id, 10, "%d", tid);
    char *path = malloc(sizeof(char) * 100);
    snprintf(path, 100, "%s%s%s%s", dir, "thread-", id, ".log");
    return path;
}

char* get_log_dir(char *root_path) {
    char formatted_time[100];
    get_formatted_time(formatted_time);
    char *dir = malloc(sizeof(char) * 100);
    snprintf(dir, 100, "%s%s%s%s", root_path, "logs/mpi/", formatted_time, "/");
    mkdir(dir, 0777);
    return dir;
}

FILE* get_log_file(char *log_dir, int rank) {
    char *path = get_filepath(log_dir, rank);
    FILE *file = fopen(path, "a+");
    return file;
}

void send_data(double **arr, int send_to, int n, int p, int send_tag) {
    double *buffer = malloc(sizeof(double) * n * p);
    for (int i = 0; i < p; i++) {
        for (int j = 0; j < n; j++) {
            buffer[i * n + j] = arr[i][j];
        }
    }
    MPI_Send(buffer, n * p, MPI_DOUBLE, send_to, send_tag, MPI_COMM_WORLD);
}

void recv_data(double **arr, int recv_from, int n, int p, int recv_tag) {
    MPI_Status status;
    double *buffer = malloc(sizeof(double) * (n * p));
    MPI_Recv(buffer, n * p, MPI_DOUBLE, recv_from, recv_tag, MPI_COMM_WORLD, &status);
    for (int i = 0; i < n * p; i++) {
        arr[(int)(ceil(i / n))][(int)(i % n)] = buffer[i];
    }
}

void init_process(double **a_arr, double **b_arr, int n, int p) {
    recv_data(a_arr, 0, n, p, A_ARR_TAG);
    recv_data(b_arr, 0, n, p, B_ARR_TAG);
}

double mult(double a_line[], double b_line[], int n) {
    double res = 0;
    for (size_t i = 0; i < n; i++) {
        res += a_line[i] * b_line[i];
    }
    return res;
};

void write_arr_to_file(FILE *file, char *message, double **arr, int rows, int cols) {
    fprintf(file, "%s\n", message);

    for (int i = 0; i < rows; i++) {
        for (int j = 0; j < cols; j++) {
            fprintf(file, "\t%.2f", arr[i][j]);
        }
        fprintf(file, "\n");
    }

    fprintf(file, "\n\n\n");
}