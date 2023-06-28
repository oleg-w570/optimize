#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include "structmember.h"

#define EPS 1e-16

typedef struct {
	PyObject_HEAD
	PyObject* lower_bound;
	PyObject* upper_bound;
    Py_ssize_t dimension;
	int evolvent_density;
} EvolventObject;

static void Evolvent_dealloc(EvolventObject* self) {
	Py_XDECREF(self->lower_bound);
	Py_XDECREF(self->upper_bound);
	Py_TYPE(self)->tp_free((PyObject*)self);
}

static PyObject* Evolvent_new(PyTypeObject* type, PyObject* args, PyObject* kwds) {
	EvolventObject* self;
	self = (EvolventObject*)type->tp_alloc(type, 0);
	if (self != NULL) {
		self->lower_bound = Py_BuildValue("[]");
		if (self->lower_bound == NULL) {
			Py_DECREF(self);
			return NULL;
		}
		self->upper_bound = Py_BuildValue("[]");
		if (self->upper_bound == NULL) {
			Py_DECREF(self);
			return NULL;
		}
		self->dimension = 0;
		self->evolvent_density = 0;
	}
	return (PyObject*)self;
}

static int Evolvent_init(EvolventObject* self, PyObject* args, PyObject* kwds) {
	static char* kwlist[] = { "lower_bound", "upper_bound", "dimension", "evolvent_density", NULL };
	PyObject* lower_bound, * upper_bound, * tmp;

	if (!PyArg_ParseTupleAndKeywords(args, kwds, "|OOii", kwlist, &lower_bound, &upper_bound, &self->dimension, &self->evolvent_density)) {
		return -1;
	}
	if (lower_bound) {
		tmp = self->lower_bound;
		Py_INCREF(lower_bound);
		self->lower_bound = lower_bound;
		Py_XDECREF(tmp);
	}
	if (upper_bound) {
		tmp = self->upper_bound;
		Py_INCREF(upper_bound);
		self->upper_bound = upper_bound;
		Py_XDECREF(tmp);
	}
	return 0;
}

static PyMemberDef Evolvent_members[] = {
	{"lower_bound", T_OBJECT_EX, offsetof(EvolventObject, lower_bound), 0, "lower bound"},
	{"upper_bound", T_OBJECT_EX, offsetof(EvolventObject, upper_bound), 0, "upper bound"},
	{"dimension", T_PYSSIZET, offsetof(EvolventObject, dimension), 0, "dimension"},
	{"evolvent_density", T_INT, offsetof(EvolventObject, evolvent_density), 0, "evolvent density"},
	{NULL}
};

Py_ssize_t calculateNode(double iis, int* u, int* v, Py_ssize_t n) {
    Py_ssize_t i;
    double nexp_extended = 1 << n;
    int iq = 1;
    Py_ssize_t n1 = n - 1;
    Py_ssize_t node = 0;

    if (fabs(iis) < EPS) {
        node = n1;
        for (i = 0; i < n; i++) {
            u[i] = -1;
            v[i] = -1;
        }
    }
    else if (fabs(iis - (nexp_extended - 1.0)) < EPS) {
        node = n1;
        u[0] = 1;
        v[0] = 1;
        for (i = 1; i < n; i++) {
            u[i] = -1;
            v[i] = -1;
        }
        v[n1] = 1;
    }
    else {
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
            }
            else {
                if (fabs(iis - iff) < EPS && fabs(iis - 1.0) > EPS) {
                    node = i;
                    iq = -1;
                }
                iis -= iff;
                k2 = 1;
            }
            j = -k1 * k2;
            u[i] = j;
            v[i] = j;
            k1 = k2;
        }
        v[node] *= iq;
        v[n1] *= -1;
    }
    return node;
}

void getYonX(double* y, Py_ssize_t n, int evolvent_density, double x) {
    double nexp_extended = 1 << n;
    int* iu = (int*)malloc(n * sizeof(int));
    int* iv = (int*)malloc(n * sizeof(int));
    int* iw = (int*)malloc(n * sizeof(int));
    int j, temp;
    double r = 0.5;
    double d = x;
    double iis;
    Py_ssize_t it = 0;
    Py_ssize_t node;
    Py_ssize_t i;

    for (i = 0; i < n; i++) {
        iu[i] = 0;
        iv[i] = 0;
        iw[i] = 1;
    }

    for (j = 0; j < evolvent_density; j++) {
        if (fabs(x - 1.0) < EPS) {
            iis = nexp_extended - 1.0;
            d = 0.0;
        }
        else {
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

void transformP2D(double* y, PyObject* lower_bound, PyObject* upper_bound, Py_ssize_t n) {
    Py_ssize_t i;
    for (i = 0; i < n; i++) {
        double l = PyLong_AsDouble(PyList_GET_ITEM(lower_bound, i));
        double u = PyLong_AsDouble(PyList_GET_ITEM(upper_bound, i));
        y[i] = y[i] * (u - l) + (u + l) / 2;
        //printf("(l=%lf, u=%lf)\t", l, u);
    }
    //printf("\n");
}

static PyObject* Evolvent_GetImage(EvolventObject* self, PyObject* args) {
    PyObject* py_y;
    double* y;
    double x;
    Py_ssize_t i;
    if (!PyArg_ParseTuple(args, "d", &x))
        return NULL;

    y = (double*)malloc(self->dimension * sizeof(double));
    for (i = 0; i < self->dimension; i++) {
        y[i] = 0.0;
    }
    getYonX(y, self->dimension, self->evolvent_density, x);
    transformP2D(y, self->lower_bound, self->upper_bound, self->dimension);

    py_y = PyList_New(self->dimension);
    for (i = 0; i < self->dimension; i++) {
        PyList_SET_ITEM(py_y, i, PyFloat_FromDouble(y[i]));
    }
    free(y);

    return py_y;
}

static PyMethodDef Evolvent_methods[] = {
    {"GetImage", (PyCFunction)Evolvent_GetImage, METH_VARARGS, "x -> y"},
    {NULL}
};

static PyTypeObject EvolventType = {
    PyVarObject_HEAD_INIT(NULL, 0)
    .tp_name = "evolvent.Evolvent",
    .tp_doc = PyDoc_STR("Evolvent class"),
    .tp_basicsize = sizeof(EvolventObject),
    .tp_itemsize = 0,
    .tp_flags = Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE,
    .tp_new = Evolvent_new,
    .tp_init = (initproc)Evolvent_init,
    .tp_free = (destructor)Evolvent_dealloc,
    .tp_members = Evolvent_members,
    .tp_methods = Evolvent_methods,
};

static PyModuleDef evolventmodule = {
    PyModuleDef_HEAD_INIT,
    .m_name = "evolvent_c",
    .m_doc = "module evolvent c implementation",
    .m_size = -1,
};

PyMODINIT_FUNC PyInit_evolvent_c(void) {
    PyObject* m;
    if (PyType_Ready(&EvolventType) < 0)
        return NULL;
    m = PyModule_Create(&evolventmodule);
    if (m == NULL)
        return NULL;

    Py_INCREF(&EvolventType);
    if (PyModule_AddObject(m, "Evolvent", (PyObject*)&EvolventType) < 0) {
        Py_DECREF(&EvolventType);
        Py_DECREF(m);
        return NULL;
    }

    return m;
}
