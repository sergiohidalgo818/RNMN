'''This file defines the InputType Enum'''

from enum import Enum
from ProcessData import ProcessError

class InputType(Enum):
    '''This enum is for the data type to train/predict '''

    TEXT = 1
    AUDIO = 2
    IMAGE = 3

class ImportError(Exception):
    '''Raised when there is an error during a file importation'''
    def __init__(self, message, *args):
        self.message = message  
        super(ImportError, self).__init__(message, *args) 