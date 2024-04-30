'''This file defines the RNMNTextModel Class'''

import numpy as np
from keras import Sequential
from .RNMNSmall import RNMNSmall

class RNMNTextModel(RNMNSmall):

    def __init__(self, data_x: np.ndarray, data_y: np.ndarray, **kwargs) -> None:
        super().__init__(data_x, data_y, **kwargs)
        
