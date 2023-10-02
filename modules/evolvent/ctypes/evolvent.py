from ctypes import *

import numpy as np


class Evolvent:
    """Класс разверток

    :param lowerBoundOfFloatVariables: массив для левых (нижних) границ, А.
    :type  lowerBoundOfFloatVariables: np.ndarray(shape = (1), dtype = np.double).
    :param upperBoundOfFloatVariables: массив для правых (верхних) границ, В.
    :type  upperBoundOfFloatVariables: np.ndarray(shape = (1), dtype = np.double).
    :param numberOfFloatVariables: размерность задачи (N).
    :type  numberOfFloatVariables: int
    :param evolventDensity: плотность развертки (m).
    :type  evolventDensity: int
    """

    lib = CDLL("modules/evolvent/ctypes/lib/evolvent.dll")

    def __init__(
        self,
        lowerBoundOfFloatVariables: np.ndarray(shape=(1), dtype=np.double) = [],
        upperBoundOfFloatVariables: np.ndarray(shape=(1), dtype=np.double) = [],
        numberOfFloatVariables: int = 1,
        evolventDensity: int = 10,
    ):
        self.numberOfFloatVariables = numberOfFloatVariables
        self.lowerBoundOfFloatVariables = np.copy(lowerBoundOfFloatVariables)
        self.upperBoundOfFloatVariables = np.copy(upperBoundOfFloatVariables)
        self.evolventDensity = evolventDensity

        self.yValues = np.zeros(self.numberOfFloatVariables, dtype=np.double)

        Evolvent.lib.getYonX.argtypes = [
            np.ctypeslib.ndpointer(np.double, ndim=1, flags="C"),
            c_size_t,
            c_int,
            c_double,
        ]

    def GetImage(self, x: np.double) -> np.ndarray(shape=(1), dtype=np.double):
        """Получить образ (x->y)

        :param x: значение x.
        :type  x: np.double.
        :return: массив значений *y*
        :rtype: np.ndarray(shape = (1), dtype = np.double).

        """

        self.__GetYonX(x)
        self.__TransformP2D()
        return np.copy(self.yValues)

    def __GetYonX(self, x: np.double):
        if self.numberOfFloatVariables == 1:
            self.yValues[0] = x - 0.5
            return self.yValues

        self.yValues = np.zeros(self.numberOfFloatVariables, dtype=np.double)
        Evolvent.lib.getYonX(
            self.yValues, self.numberOfFloatVariables, self.evolventDensity, x
        )
        return np.copy(self.yValues)

    def __TransformP2D(self):
        for i in range(0, self.numberOfFloatVariables):
            self.yValues[i] = (
                self.yValues[i]
                * (
                    self.upperBoundOfFloatVariables[i]
                    - self.lowerBoundOfFloatVariables[i]
                )
                + (
                    self.upperBoundOfFloatVariables[i]
                    + self.lowerBoundOfFloatVariables[i]
                )
                / 2
            )
