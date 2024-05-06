'''This file defines the RNMNSmall Class'''

from RNMNParent import RNMNParent
from keras import Input, layers, Model
import numpy as np
from keras.api.layers import Conv1D, MaxPooling1D, Flatten, Dense
import tensorflow
import string
import re

def custom_standardization(input_data):
    lowercase = tensorflow.strings.lower(input_data)
    return tensorflow.strings.regex_replace(
        lowercase, f"[{re.escape(string.punctuation)}]", ""
    )


class RNMNSmall(RNMNParent):

    x_train: np.ndarray
    y_train: np.ndarray
    x_test: np.ndarray
    y_test: np.ndarray
    
    num_inputs : tuple
    layers_dict: dict 

    def __init__(self, data, **kwargs) -> None:

        max_features = 20000
        embedding_dim = 128
        sequence_length = 8


        vectorize_layer = layers.TextVectorization(
        standardize=custom_standardization,
        max_tokens=max_features,
        output_mode="int",
        output_sequence_length=sequence_length,
        )

        # Let's make a text-only dataset (no labels):
        #text_ds = raw_train_ds.map(lambda x, y: x)
        # Let's call `adapt`:
        #vectorize_layer.adapt(text_ds)

        
        (self.x_train, self.y_train), (self.x_test, self.y_test) = data

        inlayer = Input(shape=(1,), dtype=tensorflow.string, name='text')
        aux_layer = vectorize_layer(inlayer)
        aux_layer = layers.Embedding(max_features, embedding_dim)(inlayer)


        if "config" in kwargs.keys():
            if "num_inputs" in kwargs["config"].keys():
                self.num_inputs = (int(kwargs["config"]['num_inputs']), )
            if "layers_dict" in kwargs["config"].keys():
                self.layers_dict = kwargs["config"]['layers_dict'] 


            dict_keys = [str(key) for key in self.layers_dict.keys()]

            dict_keys.sort()

            for key in dict_keys:
                        aux_layer = Dense(int(
                        self.layers_dict[key]['num_neurons']), self.layers_dict[key]["activation"])(aux_layer)
            
            self.model = Model(inputs=inlayer, outputs=aux_layer)
            



    def add_data_to_model(self, data:tuple):
        ((self.x_train, self.y_train ),(self.x_test, self.y_test)) = data
    