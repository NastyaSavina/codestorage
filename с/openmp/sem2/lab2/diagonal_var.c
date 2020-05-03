#include <stdio.h>
#include <omp.h>
#include <math.h>
#include <sys/stat.h>
#include <unistd.h>
#include <time.h>
#include <time.h>

#define LOG_FILE_LEN 150
#define LEN 50
#define n 100
#define t_count 1

char* get_formatted_datetime(){
    char *curr_date = malloc(sizeof(char) * LEN);
    time_t curtime = time(NULL);
    struct tm *loc_time = localtime(&curtime);
    strftime(curr_date, LEN, "%Y-%m-%dT%H:%M:%S", loc_time);
    return curr_date;
}

char* get_log_file_path(char *dir, int tid) {
    char* path = malloc(sizeof(char) * LOG_FILE_LEN);
    char id[10];

    snprintf(id, 10, "%d", tid);
    snprintf(path, 100, "%s%s%s%s", dir, "thread-", id, ".log");
    // /Users/me/programs/с/openmp/sem2/lab2/logs/2020-04-27T16:27:17/thread-1.log

    return path;
}

void prind_crud_to_file(FILE *f, double **a_arr, double *b_arr) {
    for (size_t i = 0; i < n; i++) {
        for (size_t j = 0; j < n; j++) {
            fprintf(f, "\t%.2f", a_arr[i][j]);
        }
        fprintf(f, "\t\t%.2f", b_arr[i]);
        fprintf(f, "\n");
    }
    fprintf(f, "\n\n\n\n");
}

void shuffle_if_0_found(double **a_arr, double *b_arr, int row) {
    if (a_arr[row][row] == 0) {
        for (int i = row; i < n; i++) {
            if (a_arr[row][0] != 0) {
                double temp = 0;
                for (int j = 0; j < n; j++) {
                    temp = a_arr[i][j];
                    a_arr[i][j] = a_arr[row][j];
                    a_arr[row][j] = temp;
                }
                temp = b_arr[row];
                b_arr[row] = b_arr[i];
                b_arr[i] = temp;
                return;
            }
        }
    }
}

int main() {
    clock_t begin = clock();

    double **a_arr = malloc(sizeof(double*) * n);
    
    for(int i = 0; i < n; i++) {
        a_arr[i] = malloc(sizeof(double) * n);
    }

    double *b_arr = malloc(sizeof(double) * n);

    for (size_t i = 0; i < n; i++) {
        b_arr[i] = rand() % 12 + 1;
        for (size_t j = 0; j < n; j++) {
            a_arr[i][j] = rand() % 10 + 1;
        }
    }
    
    char* formatted_datetime = get_formatted_datetime();
    char* log_dir = malloc(sizeof(char) * LOG_FILE_LEN);

    snprintf(log_dir, LOG_FILE_LEN, "%s%s%s", "/Users/me/programs/с/openmp/sem2/lab2/logs/", formatted_datetime, "/");
    mkdir(log_dir, 0777);

    char result_file_path[150];
    snprintf(result_file_path, 100, "%s%s", log_dir, "result.log");

    FILE *result_file = fopen(result_file_path, "a+");
    prind_crud_to_file(result_file, a_arr, b_arr);

    for (int fixed_row = 0; fixed_row < n; fixed_row++) {
        shuffle_if_0_found(a_arr, b_arr, fixed_row);

        double coef = a_arr[fixed_row][fixed_row];

        for (int col = fixed_row; col < n; col++) {
            a_arr[fixed_row][col] = a_arr[fixed_row][col] / coef;
        }

        b_arr[fixed_row] /= coef;

        #pragma omp parallel for shared(a_arr, b_arr) num_threads(t_count)
        for (int row = fixed_row + 1; row < n; row++) {
            int tid = omp_get_thread_num() + 1;
            char* path = get_log_file_path(log_dir, tid);
            FILE *f = fopen(path, "a+");
            fprintf(f, "for fixed row: %d \tthread: %d \tcalcuate row: %d\n", fixed_row + 1, tid, row + 1);
                
            coef = a_arr[row][0];

            for (int i = 0; i < n; i++)  a_arr[row][i] -= a_arr[fixed_row][i] * coef;

            b_arr[row] -= b_arr[fixed_row] * coef;

            fclose(f);
        }
        
        prind_crud_to_file(result_file, a_arr, b_arr);
    }



    #pragma omp parallel for shared(a_arr, b_arr) num_threads(t_count)
    for (int row = n - 1; row > -1; row--) {
        for (int col = n - 1; col > row; col--) {
            b_arr[row] -= b_arr[col] * a_arr[row][col];
            a_arr[row][col] = 0;
        }
    }
    
    prind_crud_to_file(result_file, a_arr, b_arr);

    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) {
            if (a_arr[i][j] != 0) {
                fprintf(result_file, "i%d: %.2f\n", i + 1, (b_arr[i] / a_arr[i][j]));
                break;
            }
        }
    }

    clock_t end = clock();

    double time_spend = (double)(end - begin) / CLOCKS_PER_SEC;
    
    printf("For thread count: %d system size: %d time spend(sec): %.2f\n", t_count, n, time_spend);
}