#include <stdio.h>
#include <omp.h>
#include <math.h>
#include <time.h>

int main() {
    double eps = 0.001;
    double len = 1;
    int pointCount = 4;
    double h = len / pointCount;

    double grid[pointCount][pointCount];

    clock_t t;
    t = clock();
#pragma omp parallel for shared(grid, pointCount) num_threads(2)
    for (int i = 0; i < pointCount; i++) {
        for (int j = 0; j < pointCount; j++) {
            grid[i][j] = 0;
        }
    }

#pragma omp parallel for shared(grid, pointCount) num_threads(2)
    for (int i = 0; i < pointCount; i++) {
        grid[i][0] = 1;
        grid[i][pointCount - 1] = 1;
    }

#pragma omp parallel for shared(grid, pointCount) num_threads(2)
    for (int j = 1; j < pointCount - 1; j++) {
        grid[0][j] = 1;
        grid[pointCount - 1][j] = 1;
    }

    double prev_sum = 0;

    for (int i = 0; i < pointCount; i++) {
        for (int j = 0; j < pointCount; ++j) {
            prev_sum += grid[i][j];
        }
    }

    double new_sum = 0;
    double current_eps = 0;
    do {
        new_sum = 0;
#pragma omp parallel for shared(grid, pointCount) num_threads(2)
        for (int i = 1; i < pointCount - 1; i++) {
            for (int j = 1; j < pointCount - 1; j++) {
                grid[i][j] = (grid[i - 1][j] + grid[i + 1][j] + grid[i][j - 1] + grid[i][j + 1]) / 4.;
            }
        }

        for (int i = 0; i < pointCount; i++) {
            for (int j = 0; j < pointCount; ++j) {
                new_sum += grid[i][j];
            }
        }
        current_eps = fabs(new_sum - prev_sum);
        prev_sum = new_sum;
    } while (current_eps > eps);

    t = clock() - t;
    double time_taken = ((double)t)/CLOCKS_PER_SEC; // in seconds
    for (int i = 0; i < pointCount; i++) {
        for (int j = 0; j < pointCount; j++) {
            printf("%f\t", grid[i][j]);
        }
        printf("\n");
    }
    printf("\n");
    printf("fun() took %f seconds to execute \n", time_taken);
}
