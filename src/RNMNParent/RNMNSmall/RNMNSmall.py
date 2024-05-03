'''This file defines the RNMNSmall Class'''

from RNMNParent import RNMNParent
from keras import Input, layers, Model
import numpy as np

class RNMNSmall(RNMNParent):

    data_x: np.ndarray
    data_y: np.ndarray
    
    num_inputs : tuple
    layers_dict: dict 

    def __init__(self, **kwargs) -> None:

        if "config" in kwargs.keys():
            if "num_inputs" in kwargs["config"].keys():
                self.num_inputs = (int(kwargs["config"]['num_inputs']), )
            if "layers_dict" in kwargs["config"].keys():
                self.layers_dict = kwargs["config"]['layers_dict'] 

            inlayer = Input(shape=self.num_inputs)
            if "layer_1" in self.layers_dict.keys():
                aux_layer = layers.Dense(int(self.layers_dict['layer_1']['num_neurons']), self.layers_dict['layer_1']["activation"])(inlayer)
                
                for key in self.layers_dict.keys():
                    if key != "layer_1":
                        aux_layer = layers.Dense(int(self.layers_dict[key]['num_neurons']), self.layers_dict[key]["activation"])(aux_layer)
            else:
                aux_layer = layers.Dense(int(self.layers_dict['layer_out']['num_neurons']), self.layers_dict['layer_out']["activation"])(inlayer)

            self.model = Model(inputs=inlayer, outputs=aux_layer)



    def add_data_to_model(self, data_x:np.ndarray, data_y:np.ndarray):
        self.data_x = data_x
        self.data_y = data_y