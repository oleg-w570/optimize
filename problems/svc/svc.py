from sklearn.datasets import load_breast_cancer
from sklearn.svm import SVC
from sklearn.model_selection import cross_val_score
from sklearn.utils import shuffle

from modules.utility.point import Point

from modules.utility.problem import Problem


def load_breast_cancer_data():
    dataset = load_breast_cancer()
    x_raw, y_raw = dataset['data'], dataset['target']
    inputs, outputs = shuffle(x_raw, y_raw ^ 1, random_state=42)
    return inputs, outputs


class SVC_2D(Problem):
    def __init__(self):
        super().__init__()
        self.name = 'SVC_2D'
        self.x, self.y = load_breast_cancer_data()
        regularization_value_bound = {'low': 1, 'up': 6}
        kernel_coefficient_bound = {'low': -7, 'up': -3}
        self.dim = 2
        self.lower_bound = [regularization_value_bound['low'], kernel_coefficient_bound['low']]
        self.upper_bound = [regularization_value_bound['up'], kernel_coefficient_bound['up']]
        self.optimum = Point(0, [0], 0)

    def calculate(self, point: list[float]) -> float:
        cs, gammas = point[0], point[1]
        clf = SVC(C=10 * cs, gamma=10 ** gammas)
        value = -cross_val_score(clf, self.x, self.y, scoring='f1').mean()
        return value
