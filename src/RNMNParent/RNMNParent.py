'''This file defines the RNMNAbstract abstract Class'''

from abc import ABC
from keras import Model


class RNMNParent(ABC):
    """This class is the parent class for all the model
      classes
    """

    model : Model
    
    def create_neural_model(self):
        pass

    def compile_neural_model(self):
        pass
    
    def predict(self) -> int:
        pass

    def train(self):
        pass
