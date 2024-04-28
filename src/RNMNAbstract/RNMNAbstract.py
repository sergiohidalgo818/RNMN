'''This file defines the RNMNAbstract abstract Class'''

from abc import ABC
from keras import models

class RNMNAbstract(ABC):
    """This class is the parent class for all the model
      classes
    """

    model: models.Sequential

    def create_neural_model():
        pass

    def predict()->int:
        pass

    def train():
        pass