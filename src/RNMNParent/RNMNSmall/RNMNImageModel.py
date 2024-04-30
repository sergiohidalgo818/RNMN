'''This file defines the RNMNImageModel Class'''

from .RNMNSmall import RNMNSmall 
import numpy as np

class RNMNImageModel(RNMNSmall):

    def __init__(self, data_x: np.ndarray, data_y: np.ndarray, **kwargs) -> None:
        super().__init__(data_x, data_y, **kwargs)