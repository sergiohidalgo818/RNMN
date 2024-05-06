'''This file defines the RNMNAudioModel Class'''

from .RNMNSmall import RNMNSmall 

class RNMNAudioModel(RNMNSmall):

    def __init__(self,  data, classes, config) -> None:
        super().__init__(config=config)