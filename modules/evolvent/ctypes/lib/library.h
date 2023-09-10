#ifndef EVOLVENT_LIBRARY_H
#define EVOLVENT_LIBRARY_H

#include "stddef.h"

size_t calculateNode(double iis, int* u, int* v, size_t n);

void getYonX(double *y, size_t n, int evolvent_density, double x);

#endif //EVOLVENT_LIBRARY_H
