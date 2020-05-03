#include <stdio.h>
#include <omp.h>
#include <math.h>

int main()
{
    double eps=0.001;
    double X=1;
    int N=3;
    double h=X/N;

    double U[N][N];
    #pragma omp parallel for shared(U,N) num_threads(2)
    for(int i=0; i<N; i++){
        for(int j=0; j<N; j++){
            U[i][j]=0;
        }
    }

    #pragma omp parallel for shared(U,N) num_threads(2)
    for(int i=0; i<N; i++){
        U[i][0]=i*h;
        U[i][N-1]=i*h;
    }
    #pragma omp parallel for shared(U,N) num_threads(2)
    for(int j=1; j<N-1; j++){
        U[0][j]=j*h*j*h/2;
        U[N-1][j]=j*j*h*h;
    }
    double max;
    double IterCnt = 0;
    do {
        IterCnt++;
        max = 0;
        #pragma omp parallel for shared(U,N,max) num_threads(2)
        for (int i = 1; i < N-1; i++) {
            double max0 = 0;

            for (int j = 1; j < N-1; j++) {
                double u0 = U[i][j];
                U[i][j] = 0.25*(U[i-1][j] + U[i+1][j]+ U[i][j-1] + U[i][j+1] - h*h);
                double d = fabs(U[i][j]-u0);
                if (d > max0)
                    max0 = d;
            }

            if (max0 > max)
                #pragma omp critical
            if (max0 > max)
                max = max0;
        }
    } while (max > eps);

    #pragma omp parallel for shared(U,N) num_threads(2)
    for(int i=0;i<N; i++){
        #pragma omp parallel for shared(U,N) num_threads(2)
        for(int j=0; j<N; j++){
            printf("%f:",i*h);
            printf("%f:",j*h);
            printf("%f\t",U[i][j]);
        }
        printf("\n");
    }
}
