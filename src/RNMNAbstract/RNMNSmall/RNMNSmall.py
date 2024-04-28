'''This file defines the RNMNSmall Class'''

from RNMNAbstract import RNMNAbstract
import numpy as np

class RNMNSmall(RNMNAbstract):

    data: np.ndarray

    def __init__(self, data:np.ndarray) -> None:
        self.data = data

    def predict() -> float:
        pass

    def train():
        pass