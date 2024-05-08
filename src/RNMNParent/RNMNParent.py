'''This file defines the RNMNAbstract abstract Class'''

from abc import ABC
from keras import Model


class RNMNParent(ABC):
    """This class is the parent class for all the model
      classes
    """

    model: Model

    def compile_neural_model(self, params):
        pass

    def predict(self, data) -> int:
        pass

    def train(self):
        pass
