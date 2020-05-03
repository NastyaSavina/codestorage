#include <stdio.h>
#include <omp.h>
#include <math.h>
#include <sys/stat.h>
#include <unistd.h>
#include <time.h>

#define LEN 50
void get_formatted_time(char *curr_date){
   char buf[LEN];
   time_t curtime;
   struct tm *loc_time;
 
   curtime = time (NULL);
 
   loc_time = localtime (&curtime);

   strftime(curr_date, LEN, "%Y-%m-%dT%H:%M:%S", loc_time);

}

double mult(double a_line[], double b_line[], int n) {
    double res = 0;

    for (size_t i = 0; i < n; i++) {
        res += a_line[i] * b_line[i];
    }
    
    return res;
};

void get_filepath(char *path, char *dir, int tid) {
    char id[10];
    snprintf(id, 10, "%d", tid);
    snprintf(path, 100, "%s%s%s%s", dir, "thread-", id, ".log");
}

int main() {
    int n = 30;
    int t_count = 5;

    // double *a_arr = malloc(sizeof(*double) * n);
    // for (int i = 0; i < n; i++) {
    //     a_arr[i] = malloc(sizeof(double) * n);
    // }

    // double *b_arr = malloc(sizeof(*double) * n);
    // for (int i = 0; i < n; i++) {
    //     b_arr[i] = malloc(sizeof(double) * n);
    // }

    double a_arr[n][n];
    double b_arr[n][n];
    double res_arr[n][n];

    for (size_t i = 0; i < n; i++) {
        for (size_t j = 0; j < n; j++) {
            b_arr[i][j] = (j + 1) + (i) * n;
            a_arr[i][j] = (j + 1) + (i) * n;
            printf("\t%f", b_arr[i][j]);
        }
        printf("\n");
    }
    init_a_arr(&a_arr);
    init_b_arr(&b_arr);
    
    char a[100];
    get_formatted_time(a);
    char dir[150];
    snprintf(dir, 100, "%s%s%s", "/Users/me/programs/с/openmp/sem2/lab1/logs/", a, "/");
    mkdir(dir, 0777);

    #pragma omp parallel for shared(a_arr, b_arr, res_arr) num_threads(t_count)
    for (size_t i = 0; i < n; i++) {
        char path[150];
        int tid = omp_get_thread_num();
        get_filepath(path, dir, omp_get_thread_num());
        FILE *f = fopen(path, "a+");
        fprintf(f, "Thread %d got %zu line of A array\n", tid, i);
        
        for (size_t j = 0; j < n; j++) {
            double a_row[n];
            double b_col[n];
            for (size_t k = 0; k < n; k++) {
                a_row[k] = a_arr[i][k];
                b_col[k] = b_arr[k][j];
            }
            res_arr[i][j] = mult(a_row, b_col, n);
        }
        fprintf(f, "Thread %d calculated %zu line of result array\n", tid, i);
    }

    char path[150];
    snprintf(path, 100, "%s%s", dir, "result.log");
    FILE *f = fopen(path, "a+");
    for (size_t i = 0; i < n; i++) {
        for (size_t j = 0; j < n; j++) {
            fprintf(f, "\t%.2f", res_arr[i][j]);
        }
        fprintf(f, "\n");
    }
    
}