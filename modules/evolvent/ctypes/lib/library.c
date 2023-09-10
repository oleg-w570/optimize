#include "library.h"

#include "stdlib.h"
#include "math.h"
#include "stdio.h"

#define EPS 1e-16

size_t calculateNode(double iis, int *u, int *v, size_t n) {
    double nexp_extended = 1 << n;
    int iq = 1;
    size_t n1 = n - 1;
    size_t node = 0;
    size_t i;

    if (fabs(iis) < EPS) {
        node = n1;
        for (i = 0; i < n; i++) {
            u[i] = -1;
            v[i] = -1;
        }
    } else if (fabs(iis - (nexp_extended - 1.0)) < EPS) {
        node = n1;
        u[0] = 1;
        v[0] = 1;
        for (i = 1; i < n; i++) {
            u[i] = -1;
            v[i] = -1;
        }
        v[n1] = 1;
    } else {
        double iff = nexp_extended;
        int k1 = -1;
        for (i = 0; i < n; i++) {
            int k2;
            int j;
            iff *= 0.5;
            if (iis < iff) {
                k2 = -1;
                if (fabs(iis - (iff - 1.0)) < EPS && fabs(iis) > EPS) {
                    node = i;
                    iq = 1;
                }
            } else {
                if (fabs(iis - iff) < EPS && fabs(iis - 1.0) > EPS) {
                    node = i;
                    iq = -1;
                }
                iis -= iff;
                k2 = 1;
            }
            j = - k1 * k2;
            u[i] = j;
            v[i] = j;
            k1 = k2;
        }
        v[node] *= iq;
        v[n1] *= -1;
    }
    return node;
}

void getYonX(double *y, size_t n, int evolvent_density, double x) {
    double nexp_extended = 1 << n;
    int *iu = (int*)malloc(n * sizeof(int));
    int *iv = (int*)malloc(n * sizeof(int));
    int *iw = (int*)malloc(n * sizeof(int));
    int j, temp;
    double r = 0.5;
    double d = x;
    double iis;
    size_t it = 0;
    size_t node;
    size_t i;

    for (i = 0; i < n; i++) {
        iu[i] = 0;
        iv[i] = 0;
        iw[i] = 1;
    }

    for (j = 0; j < evolvent_density; j++) {
        if (fabs(x - 1.0) < EPS) {
            iis = nexp_extended - 1.0;
            d = 0.0;
        } else {
            d *= nexp_extended;
            d = modf(d, &iis);
        }

        node = calculateNode(iis, iu, iv, n);

        temp = iu[0];
        iu[0] = iu[it];
        iu[it] = temp;

        temp = iv[0];
        iv[0] = iv[it];
        iv[it] = temp;

        if (node == 0)
            node = it;
        else if (node == it)
            node = 0;

        r *= 0.5;
        it = node;
        for (i = 0; i < n; i++) {
            iu[i] *= iw[i];
            iw[i] *= -iv[i];
            y[i] += r * iu[i];
        }
    }
    free(iu);
    free(iv);
    free(iw);
}



























