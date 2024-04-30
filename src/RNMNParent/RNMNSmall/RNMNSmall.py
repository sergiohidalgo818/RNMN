'''This file defines the RNMNSmall Class'''

from RNMNParent import RNMNParent
from keras import Input, layers, Model
import numpy as np

class RNMNSmall(RNMNParent):

    data_x: np.ndarray
    data_y: np.ndarray
    
    entry_layer : tuple
    layers_list: list # a list of tuples like (neurons, activation)


    def __init__(self, **kwargs) -> None:


        if "entry_layer" in kwargs.keys():
            self.entry_layer = kwargs['entry_layer'] 
        if "layers_dict" in kwargs.keys():
            self.layers_dict = kwargs['layers_dict'] 

        inlayer = Input(shape=self.entry_layer)

        aux_layer = layers.Dense(self.layers_list[0][0], self.layers_list[0][1]) (inlayer)

        for x in range(1, len(self.layers_list)):
            aux_layer = layers.Dense(self.layers_list[x][0], self.layers_list[x][1]) (aux_layer)

        self.model = Model(inputs=inlayer, outputs=aux_layer)

    def add_data_to_model(self, data_x:np.ndarray, data_y:np.ndarray):
        self.data_x = data_x
        self.data_y = data_y