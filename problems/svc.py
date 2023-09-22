from sklearn.svm import SVC
from sklearn.model_selection import cross_val_score


class SVC_2D:
    def __init__(self,
                 x_dataset: list[float],
                 y_dataset: list[float],
                 regularization_value_bound: dict[str, float],
                 kernel_coefficient_bound: dict[str, float]):
        self.x = x_dataset
        self.y = y_dataset
        self.lower_bound = [regularization_value_bound['low'], kernel_coefficient_bound['low']]
        self.upper_bound = [regularization_value_bound['up'], kernel_coefficient_bound['up']]

    def calculate(self, point: list[float]):
        cs, gammas = point[0], point[1]
        clf = SVC(C=10 * cs, gamma=10 ** gammas)
        value = -cross_val_score(clf, self.x, self.y, scoring='f1').mean()
        return value
