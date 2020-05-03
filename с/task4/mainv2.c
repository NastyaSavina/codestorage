#include <stdio.h>
#include <omp.h>
#include <math.h>
#include <time.h>

double f(double x, double y) {
    return 0;
}

int main() {
    double eps = 0.001;
    double len = 1;
    int pointCount = 300;
    int thread_num = 5;
    double h = len / pointCount;

    double grid[pointCount][pointCount];

    clock_t t;
    t = clock();
#pragma omp parallel for shared(grid, pointCount) num_threads(thread_num)
    for (int i = 0; i < pointCount; i++) {
        for (int j = 0; j < pointCount; j++) {
            grid[i][j] = 0;
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

    double max_eps;
    double current_max_eps;
    double prev_val;
    double point_eps;
    int step_count = 0;
    do {
        max_eps = 0;
#pragma omp parallel for shared(grid,pointCount,max_eps) num_threads(thread_num)
        for (int i = 1; i < pointCount-1; i++) {
            current_max_eps = 0;
            for (int j = 1; j < pointCount-1; j++) {
                prev_val = grid[i][j];
                grid[i][j] = (grid[i-1][j] + grid[i+1][j]+ grid[i][j-1] + grid[i][j+1]) / 4.;
                point_eps = fabs(grid[i][j] - prev_val);
                if (point_eps > current_max_eps) {
                    current_max_eps = point_eps;
                }
            }

#pragma omp critical
            if (current_max_eps > max_eps) {
                max_eps = current_max_eps;
            }
        }
        printf("%d\n", ++step_count);
        printf("%f\n", max_eps);
    } while (max_eps > eps);

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

