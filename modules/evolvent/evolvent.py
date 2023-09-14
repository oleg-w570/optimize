import numpy as np
import math


class Evolvent:
    """Класс разверток

    :param lower_bound: массив для левых (нижних) границ, А.
    :type  lower_bound: np.ndarray(shape = (1), dtype = np.double).
    :param upper_bound: массив для правых (верхних) границ, В.
    :type  upper_bound: np.ndarray(shape = (1), dtype = np.double).
    :param dimension: размерность задачи (N).
    :type  dimension: int
    :param evolvent_density: плотность развертки (m).
    :type  evolvent_density: int
    """

    def __init__(self,
                 lower_bound: np.ndarray = [],
                 upper_bound: np.ndarray = [],
                 dimension: int = 1,
                 evolvent_density: int = 10
                 ):
        self.dim = dimension
        self.lower_bound = np.copy(lower_bound)
        self.upper_bound = np.copy(upper_bound)
        self.evolvent_density = evolvent_density

        self.nexp_value = 0
        self.nexp_extended: float = 1.0

        self.yValues = np.zeros(self.dim, dtype=np.double)
        for i in range(0, self.dim):
            self.nexp_extended += self.nexp_extended

    def get_image(self,
                  x: float
                  ) -> np.ndarray:
        """Получить образ (x->y)

        :param x: значение x.
        :type  x: np.double.
        :return: массив значений *y*
        :rtype: np.ndarray(shape = (1), dtype = np.double).

        """

        self.__y_on_x(x)
        self.__transform_p2d()
        return np.copy(self.yValues)

    def __transform_p2d(self):
        for i in range(0, self.dim):
            self.yValues[i] = self.yValues[i] * (
                    self.upper_bound[i] - self.lower_bound[i]) + \
                              (self.upper_bound[i] + self.lower_bound[i]) / 2

    def __y_on_x(self, _x: float) -> np.ndarray:
        if self.dim == 1:
            self.yValues[0] = _x - 0.5
            return self.yValues

        d = _x
        r: float = 0.5
        it: int = 0

        iw = np.ones(self.dim, dtype=np.int32)
        self.yValues = np.zeros(self.dim, dtype=np.double)
        iu = np.zeros(self.dim, dtype=np.int32)
        iv = np.zeros(self.dim, dtype=np.int32)

        for j in range(0, self.evolvent_density):
            if math.isclose(_x, 1.0):
                iis = self.nexp_extended - 1.0
                d = 0.0
            else:
                d *= self.nexp_extended
                iis = int(d)
                d -= iis

            node = self.__calculate_node(iis, self.dim, iu, iv)

            iu[0], iu[it] = iu[it], iu[0]
            iv[0], iv[it] = iv[it], iv[0]

            if node == 0:
                node = it
            elif node == it:
                node = 0

            r *= 0.5
            it = node
            for i in range(0, self.dim):
                iu[i] *= iw[i]
                iw[i] *= -iv[i]
                self.yValues[i] += r * iu[i]

        return np.copy(self.yValues)

    def __calculate_node(self,
                         iis: float,
                         n: int,
                         u: np.ndarray,
                         v: np.ndarray,
                         ):

        iq = 1
        n1 = n - 1
        node = 0
        if math.isclose(iis, 0.0):
            node = n1
            for i in range(0, n):
                u[i] = -1
                v[i] = -1
        elif math.isclose(iis, self.nexp_extended - 1.0):
            node = n1
            u[0] = 1
            v[0] = 1
            for i in range(1, n):
                u[i] = -1
                v[i] = -1
            v[n1] = 1
        else:
            iff = self.nexp_extended
            k1 = -1
            for i in range(0, n):
                iff /= 2
                if iis < iff:  # исправить сравнение!
                    k2 = -1
                    if math.isclose(iis, (iff - 1.0)) and not math.isclose(iis, 0.0):
                        node = i
                        iq = 1
                else:
                    if math.isclose(iis, iff) and not math.isclose(iis, 1.0):
                        node = i
                        iq = -1
                    iis -= iff
                    k2 = 1
                j = -k1 * k2
                v[i] = j
                u[i] = j
                k1 = k2
            v[node] *= iq
            v[n1] *= -1
        return node
