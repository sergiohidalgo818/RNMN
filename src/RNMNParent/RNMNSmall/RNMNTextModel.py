'''This file defines the RNMNTextModel Class'''

from .RNMNSmall import RNMNSmall
from RNMNApp import InputType

class RNMNTextModel(RNMNSmall):

    def __init__(self,  data,  config) -> None:
        super().__init__(data, config=config)
        
