'''This file defines the InputType Enum'''

from enum import Enum

class InputType(Enum):
    '''This enum is for the data type to train/predict '''

    TEXT = 1
    AUDIO = 2
    IMAGE = 3