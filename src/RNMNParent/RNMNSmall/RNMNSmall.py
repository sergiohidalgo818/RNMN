'''This file defines the RNMNSmall Class'''

from RNMNParent import RNMNParent

import numpy as np



class RNMNSmall(RNMNParent):

    x_train: np.ndarray
    y_train: np.ndarray
    x_test: np.ndarray
    y_test: np.ndarray
    
    num_inputs : tuple
    layers_dict: dict 

    def __init__(self, data, **kwargs) -> None:
        (self.x_train, self.y_train), (self.x_test, self.y_test) = data

  


    def add_data_to_model(self, data:tuple):
        ((self.x_train, self.y_train ),(self.x_test, self.y_test)) = data
    