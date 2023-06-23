#ifndef EVOLVENT_LIBRARY_H
#define EVOLVENT_LIBRARY_H

#include "stddef.h"

size_t calculateNode(double nexp_extended, double iis, int* u, int* v, size_t n);

void getYonX(double x, double *y, size_t n, double nexp_extended, int evolvent_density);

#endif //EVOLVENT_LIBRARY_H
