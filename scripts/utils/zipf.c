/**
 * zipf.c is a small script that generates data from a zipfian distribution with
 * skewness parameter "z" 
 *
 */
#include <stdio.h>
#include <math.h>
#include <stdlib.h>

void get_zipf(float, int); /* the zipf probability generator function */

struct probvals {
    float prob; /* the access probability */
    float cum_prob; /* the cumulative access probability */
};

struct probvals *zdist; /* the probability distribution  */

int main(int argc, char** argv) {
    int i, j, nSamps;
    float z; /* the skew parameter */
    int N; /* the number of objects */
    double randProbe;   /* used for generating random numbers */

    if (argc < 3) {
        printf("Usage: zipf <z N nSamps> \n");
        exit(0);
    }

    z = atof(argv[1]);
    N = atoi(argv[2]);
    nSamps = atoi(argv[3]);

    if (N <= 0) {
        printf("Error in parameters \n");
        exit(0);
    }

    zdist = (struct probvals *) malloc(N * sizeof(struct probvals));

    get_zipf(z, N); /* generate the distribution */

    // now we want to draw random numbers from the probability distribution
    for (i = 0; i < nSamps; i++) {
        randProbe = (double)rand() / (double)RAND_MAX;  // randProbe \in [0, 1]

        for (j = 0; j < N; j++) {      /* search for number */
            if (zdist[j].cum_prob > randProbe) {
                break;
            }
        }
        printf("%d\n", j);
    }
}

void get_zipf(float z, int N) {
    float sum = 0.0;
    float c = 0.0;
    float expo;
    float sumc = 0.0;
    int i;

    expo = z;

    /*
     * zipfian - p(i) = c / i ^^ (1 - theta) At x
     * = 1, uniform * at x = 0, pure zipfian
     */

    for (i = 1; i <= N; i++) {
        sum += 1.0 / (float) pow((double) i, (double) (expo));
    }
    c = 1.0 / sum;

    for (i = 0; i < N; i++) {
        zdist[i].prob = c / (float) pow((double) (i + 1), (double) (expo));
        sumc += zdist[i].prob;
        zdist[i].cum_prob = sumc;
    }

}
