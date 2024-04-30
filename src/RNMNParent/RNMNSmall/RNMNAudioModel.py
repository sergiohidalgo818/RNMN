'''This file defines the RNMNAudioModel Class'''

import numpy as np
from .RNMNSmall import RNMNSmall 

class RNMNAudioModel(RNMNSmall):

    def __init__(self, data_x: np.ndarray, data_y: np.ndarray, **kwargs) -> None:
        super().__init__(data_x, data_y, **kwargs)
        