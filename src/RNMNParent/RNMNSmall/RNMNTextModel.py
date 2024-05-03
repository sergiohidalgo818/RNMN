'''This file defines the RNMNTextModel Class'''

import numpy as np
from keras import Sequential
from .RNMNSmall import RNMNSmall

class RNMNTextModel(RNMNSmall):

    def __init__(self, config) -> None:
        super().__init__(config=config)
        
