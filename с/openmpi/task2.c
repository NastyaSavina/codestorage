#include<mpi.h>
#include<stdio.h>

struct borders {
    double left;
    double right;
};

double f (double x) {
    return x * x;
}

double integr(double left, double right) {
    const int STEP_COUNT = 10;
    double step = (right - left) / STEP_COUNT;
    double sum = 0;

    for (int i = 0; i < STEP_COUNT; i++) {
        double leftBorder = left + i * step;
        double rightBorder = left + (i + 1) * step;
        sum += (f(rightBorder) + f(leftBorder)) / 2 * step;
    }

    return sum;
}

int main(int argc, char **argv) {
    const int TAG_WANT_BORDERS = 200;
    const int TAG_NEXT_BORDER = 100;
    const int TAG_STOP = 404;
    const int SOURCE_MASTER = 0;
    int myrank;
    int slaves;

    MPI_Init(&argc, &argv);
    MPI_Comm_rank(MPI_COMM_WORLD,&myrank);
    MPI_Comm_size(MPI_COMM_WORLD,&slaves);

    if (myrank == SOURCE_MASTER) {
        double start = 0;
        double end = 100;
        int stepCount = 20;
        double stepLen = (end - start) / (double)stepCount;
        printf("Step len: %f\n\n", stepLen);

        // 5  5  5  5  5  5
        // 0  1  2  3  4  5
        // 1  2  3  4  5  6
        // 0  5 10 15 20 25 ...
        // 5 10 15 20 25 30 ...

        struct borders borderArr[stepCount];

        for (int i = 0; i < stepCount; i++) {
            struct borders border = { stepLen * i, stepLen * (i+1) };
            borderArr[i] = border;
        }

        for (int i = 0; i < stepCount; i++) {
            printf("Border №%d:\n\tLeft: %f \n\tRight: %f \n\n", i + 1, borderArr[i].left, borderArr[i].right);
        }

        double integral = 0;
        double buffer = 0;
        MPI_Status status;
        int currentStepNumber = 0;
        
        while (currentStepNumber < stepCount) {
            MPI_Recv(&buffer, 1, MPI_DOUBLE, 
                    MPI_ANY_SOURCE, TAG_WANT_BORDERS, 
                    MPI_COMM_WORLD, &status);
                    
            integral += buffer;
            
            int slaveNumber = status.MPI_SOURCE;
            printf("current step number: %d \n\t", currentStepNumber + 1);
            printf("slave: %d\n\t", slaveNumber);

            printf("left: %f\n\t", borderArr[currentStepNumber].left);
            printf("right: %f\n\n", borderArr[currentStepNumber].right);
            double buffer[] = { borderArr[currentStepNumber].left, borderArr[currentStepNumber].right };
            MPI_Send(buffer, 2, MPI_DOUBLE, slaveNumber, TAG_NEXT_BORDER, MPI_COMM_WORLD);
            currentStepNumber++;
        }

        int stopSignalCount = 0;
        const double END_ARR[] = {0, 0};
        while (stopSignalCount < slaves-1) {
            MPI_Recv(&buffer, 1, MPI_DOUBLE, 
                    MPI_ANY_SOURCE, TAG_WANT_BORDERS, 
                    MPI_COMM_WORLD, &status);

            integral += buffer;
            int slaveNumber = status.MPI_SOURCE;

            MPI_Send(END_ARR, 2, MPI_DOUBLE, slaveNumber, TAG_STOP, MPI_COMM_WORLD);
            
            stopSignalCount++;
        }

        printf("\nMaster finish calculation\nIntegral is equals to: %f\n", integral);
    } else {
            printf("try to recv");
        const int NEED_MORE = 1;
        const double START = 0;
        double res;
        int count = 0;
        double borders[2];

        MPI_Status status;

        printf("Process %d created\n", myrank);

        MPI_Send(&START, 1, MPI_DOUBLE, SOURCE_MASTER, TAG_WANT_BORDERS, MPI_COMM_WORLD);

        while (NEED_MORE) {

            MPI_Recv(borders, 2, MPI_DOUBLE, SOURCE_MASTER, MPI_ANY_TAG, MPI_COMM_WORLD, &status);

            if (status.MPI_TAG != TAG_STOP) {

                res = integr(borders[0], borders[1]);

                MPI_Send(&res, 1, MPI_DOUBLE, SOURCE_MASTER, TAG_WANT_BORDERS, MPI_COMM_WORLD);
                count++;
            } else {
                printf("\nProcess %d end calculation: count %d borders\n", myrank, count);
                break;
            }
        }
    }

    MPI_Finalize();
}