'''This file defines the RNMNTextModel Class'''

from .RNMNSmall import RNMNSmall
from RNMNApp import InputType

class RNMNTextModel(RNMNSmall):

    def __init__(self,  data, classes, config) -> None:
        super().__init__(config=config)
        
