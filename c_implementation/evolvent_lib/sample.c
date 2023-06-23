#include "stdlib.h"
#include "library.h"
#include "stdio.h"
#include "time.h"
#include "unistd.h"

int main() {
    size_t n = 2;
    size_t i;
    double x = 0.991;
    clock_t start = clock(), end;
    double *y = (double*)malloc(n);
    for (i = 0; i < n; i++) {
        y[i] = 0.0;
    }
    getYonX(x, y, n, 4.0, 10);
    end = clock();
    printf("%.20f\n",((double)end - (double)start) / (CLOCKS_PER_SEC));
    for (i = 0; i < n; ++i) {
        printf("%.8lf ", y[i]);
    }

    return 0;
}