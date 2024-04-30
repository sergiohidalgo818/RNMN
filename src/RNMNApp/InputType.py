'''This file defines the InputType Enum'''

from enum import Enum

class InputType(Enum):
    '''This enum is for the data type to train/predict '''

    TEXT = "text"
    AUDIO = "audio"
    IMAGE = "image"

class ImportError(Exception):
    '''Raised when there is an error during a file importation'''
    def __init__(self, message, *args):
        self.message = message  
        super(ImportError, self).__init__(message, *args) 