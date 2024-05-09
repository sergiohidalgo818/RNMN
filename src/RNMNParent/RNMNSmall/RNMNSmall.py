'''This file defines the RNMNSmall Class'''

from RNMNParent import RNMNParent
from ..RNMNParams import RNMNLayers
from ..RNMNParams import ParamError

import numpy as np
from keras.api.models import Model
from keras.api import KerasTensor


class RNMNSmall(RNMNParent):
    """Parent class of all the models
    """

    x_train: np.ndarray
    y_train: np.ndarray
    x_test: np.ndarray
    y_test: np.ndarray

    num_inputs: tuple
    layers_dict: dict
    in_layer: KerasTensor

    def __init__(self) -> None:
        """Initializes the model layers, expects that the
          input layer is already created
        """
        self.model = Model()

        self.layers_dict = self.create_layers_dict(self.layers_dict)

        dict_keys = [str(layer) for layer in self.layers_dict.keys()]

        dict_keys.sort()

        if 'layer_1' in dict_keys:
            aux_layer = self.layers_dict['layer_1']['fun'](
                **self.layers_dict['layer_1']['params'])(self.in_layer)
            for layer in dict_keys:
                if 'layer_1' != layer:
                    aux_layer = self.layers_dict[layer]['fun'](
                        **self.layers_dict[layer]['params'])(aux_layer)

        self.model = Model(inputs=self.in_layer, outputs=aux_layer)

    def create_layers_dict(self, layers_dict):
        final_layers = dict()
        options_layers = RNMNLayers.gen_options_layers()
        if "layer_out" not in layers_dict.keys():
            raise ParamError("No out layer")
        for layer in layers_dict.keys():
            final_layers[layer] = dict()
            if "type" not in layers_dict[layer].keys():
                raise ParamError("Layer has no type")

            final_layers[layer]['params'] = layers_dict[layer]['params']
            final_layers[layer]['fun'] = options_layers[RNMNLayers(
                layers_dict[layer]['type'])]

        return final_layers

    def add_data_to_model(self, data: tuple):
        ((self.x_train, self.y_train), (self.x_test, self.y_test)) = data
