'''This file defines the RNMNAudioModel Class'''

from .RNMNSmall import RNMNSmall 

class RNMNAudioModel(RNMNSmall):
    """Class of the audio model
    """

    def __init__(self,  data,  config) -> None:
        super().__init__()