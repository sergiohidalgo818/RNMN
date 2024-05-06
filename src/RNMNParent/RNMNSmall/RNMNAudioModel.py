'''This file defines the RNMNAudioModel Class'''

from .RNMNSmall import RNMNSmall 

class RNMNAudioModel(RNMNSmall):

    def __init__(self,  data,  config) -> None:
        super().__init__(config=config)