#include <stdio.h>
#include <omp.h>
#include <time.h>
#include <math.h>

double f(double x, double y) {
    return 0;
}

int main() {
    double eps = 0.001;
    double len = 1;
    int pointCount = 5;
    double h = len / (pointCount - 1);
    int thread_num = 3;

    double grid[pointCount][pointCount];

    clock_t t;
    t = clock();
#pragma omp parallel for shared(grid, pointCount) num_threads(thread_num)
    for (int i = 1; i < pointCount - 1; i++) {
        for (int j = 1; j < pointCount - 1; j++) {
            grid[i][j] = f(i * h, j * h);
        }
    }

#pragma omp parallel for shared(grid, pointCount) num_threads(thread_num)
    for (int i = 0; i < pointCount; i++) {
        grid[i][0] = 1;
        grid[i][pointCount - 1] = 1;
    }

#pragma omp parallel for shared(grid, pointCount) num_threads(thread_num)
    for (int j = 1; j < pointCount - 1; j++) {
        grid[0][j] = 1;
        grid[pointCount - 1][j] = 1;
    }
    double prev_sum = 0;

#pragma omp parallel for reduction (+:prev_sum) num_threads(thread_num)
    for (int i = 0; i < pointCount; i++) {
        for (int j = 0; j < pointCount; j++) {
            prev_sum += grid[i][j];
        }
    }

    double new_sum = 0;
    double current_eps = 0;
    int step_count = 0;
    int start_line = 0;
    do {
        new_sum = 0;
        start_line = (step_count % 2) + 1;
#pragma omp parallel for shared(grid, pointCount) num_threads(thread_num)
        for (int i = start_line; i < pointCount - 1; i++) {
            for (int j = 1; j < pointCount - 1; j++) {
                grid[i][j] = (grid[i - 1][j] + grid[i + 1][j] + grid[i][j - 1] + grid[i][j + 1]) / 4.;
            }
        }

#pragma omp parallel for reduction (+:new_sum) num_threads(thread_num)
        for (int i = 0; i < pointCount; i+=2) {
            for (int j = 0; j < pointCount; j+=2) {
                new_sum += grid[i][j];
            }
        }

        current_eps = fabs(new_sum - prev_sum);
        prev_sum = new_sum;
        printf("%d\n", ++step_count);
        printf("%f\n", current_eps);
    } while (current_eps > eps);


    t = clock() - t;
    for (int i = 0; i < pointCount; i++) {
        for (int j = 0; j < pointCount; j++) {
            printf("%f\t", grid[i][j]);
        }
        printf("\n");
    }
    printf("\n");

    double time_taken = ((double)t)/CLOCKS_PER_SEC; // in seconds
    printf("fun() took %f seconds to execute \n", time_taken);
}
//
// Created by Aliaksandr Zaparozhtsau on 1/21/20.
//

