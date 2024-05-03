'''This file defines the RNMNAudioModel Class'''

import numpy as np
from .RNMNSmall import RNMNSmall 

class RNMNAudioModel(RNMNSmall):

    def __init__(self, config) -> None:
        super().__init__(config=config)