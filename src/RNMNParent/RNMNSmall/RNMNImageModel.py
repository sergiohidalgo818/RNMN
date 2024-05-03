'''This file defines the RNMNImageModel Class'''

from .RNMNSmall import RNMNSmall 
import numpy as np

class RNMNImageModel(RNMNSmall):

    def __init__(self, config) -> None:
        super().__init__(config=config)