#include <stdio.h>
#include <omp.h>
#include <math.h>
#include <sys/stat.h>
#include <unistd.h>
#include <time.h>
#include <time.h>

#define LOG_FILE_LEN 150
#define LEN 50
#define n 50
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

void prind_crud_to_file(FILE *f, double a_arr[n][n], double b_arr[n]) {
    for (size_t i = 0; i < n; i++) {
        for (size_t j = 0; j < n; j++) {
            fprintf(f, "\t%.2f", a_arr[i][j]);
        }
        fprintf(f, "\t\t%.2f", b_arr[i]);
        fprintf(f, "\n");
    }
    fprintf(f, "\n\n\n\n");
}

int main() {

    clock_t begin = clock();

    double a_arr[n][n];
    double b_arr[n];

    for (size_t i = 0; i < n; i++) {
        b_arr[i] = rand() % 12 + 1;
        for (size_t j = 0; j < n; j++) {
            a_arr[i][j] = rand() % 10 + 1;
        }
    }
    
    char* a = get_formatted_datetime();
    char* log_dir = malloc(sizeof(char) * LOG_FILE_LEN);

    snprintf(log_dir, LOG_FILE_LEN, "%s%s%s", "/Users/me/programs/с/openmp/sem2/lab2/logs/", a, "/");
    mkdir(log_dir, 0777);

    char* init_log_file = malloc(sizeof(char) * LOG_FILE_LEN);
    snprintf(init_log_file, LOG_FILE_LEN, "%s%s", log_dir, "init.log");

    FILE *init_file = fopen(init_log_file, "a+");
    prind_crud_to_file(init_file, a_arr, b_arr);

    char result_file_path[150];
    snprintf(result_file_path, 100, "%s%s", log_dir, "result.log");

    FILE *result_file = fopen(result_file_path, "a+");
    prind_crud_to_file(result_file, a_arr, b_arr);

    int already_used_lines_indexes[n];
    for (int i = 0; i < n; i++) {
        already_used_lines_indexes[i] = 0;
    }

    for (size_t k = 0; k < n; k++) {

        int not_null_line = 0;
        
        for (int i = 0; i < n; i++) {
            if (a_arr[i][k] != 0) {
                int is_used_line = 0;
                for(int j = 0; j < k; j++) {
                    if (i == already_used_lines_indexes[j]) {
                        is_used_line = 1;
                        break;
                    } 
                }
                
                if (!is_used_line) {    
                    not_null_line = i;
                    already_used_lines_indexes[k] = i;
                    break;
                }
            }
        }


        #pragma omp parallel for shared(a_arr, b_arr) num_threads(t_count)
        for (size_t i = 0; i < n; i++) {

            int tid = omp_get_thread_num() + 1;
            char* path = get_log_file_path(log_dir, tid);
            FILE *f = fopen(path, "a+");
            fprintf(f, "for col: %lu \tdepending on line: %d \tthread: %d \tcalcuate line: %zu\n", k + 1, not_null_line + 1, tid, i + 1);
            
            if (i != not_null_line) {
                double coef = a_arr[i][k] / a_arr[not_null_line][k];
                
                for(int j = k; j < n; j++) {
                    a_arr[i][j] = a_arr[i][j] - a_arr[not_null_line][j] * coef;
                }

                b_arr[i] = b_arr[i] - b_arr[not_null_line] * coef;
            }
            
            fclose(f);
        }
        
        prind_crud_to_file(result_file, a_arr, b_arr);
    }

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