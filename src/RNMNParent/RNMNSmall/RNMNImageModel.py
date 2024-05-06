'''This file defines the RNMNImageModel Class'''

from .RNMNSmall import RNMNSmall
from keras import Input
from keras.api.datasets import mnist
import numpy as np
from keras.api.layers import Conv2D, MaxPooling2D, Flatten, Dense
from keras.api.models import Sequential, Model
from keras.api.losses import categorical_crossentropy


class RNMNImageModel(RNMNSmall):

    def __init__(self, data, config) -> None:

        if "num_inputs" in config.keys():
            self.num_inputs = (int(config['num_inputs']), )
        if "layers_dict" in config.keys():
            self.layers_dict = config['layers_dict']

        self.model = Model()


        (self.x_train, self.y_train), (self.x_test, self.y_test) = data

        inlayer = Input(shape=self.x_train.shape[
                1:])
        aux_layer = Conv2D(filters=6, kernel_size=(
                5, 5), activation='relu', padding='same', input_shape=self.x_train.shape[
                1:])(inlayer)
        
        aux_layer = MaxPooling2D()(inlayer) 
        
        aux_layer = Conv2D(filters=16, kernel_size=(5, 5), activation='relu')(aux_layer)
        aux_layer= MaxPooling2D()(aux_layer)
        
        aux_layer = Flatten()(aux_layer)

        # TO-DO implement file with default layers (120 and 84 in this case)
        dict_keys = [str(key) for key in self.layers_dict.keys()]

        dict_keys.sort()

        for key in dict_keys:
                    aux_layer = Dense(int(
                        self.layers_dict[key]['num_neurons']), self.layers_dict[key]["activation"])(aux_layer)

        self.model = Model(inputs=inlayer, outputs=aux_layer)

