'''This file defines the RNMNTextModel Class'''

from .RNMNSmall import RNMNSmall
from keras import Input, layers, Model
from RNMNApp import InputType
from keras.api.layers import Conv1D, MaxPooling1D, Flatten, Dense
import tensorflow
import re
import string

class RNMNTextModel(RNMNSmall):

    

    def vectorize_text(self, text, label):
        text = tensorflow.expand_dims(text, -1)
        return self.vectorize_layer(text), label
    
    
    def custom_standardization(self, input_data):
        lowercase = tensorflow.strings.lower(input_data)
        return tensorflow.strings.regex_replace(
            lowercase, f"[{re.escape(string.punctuation)}]", ""
    )

    def __init__(self,  data,  config) -> None:
        
        
        max_features = 20000
        embedding_dim = 128
        sequence_length = 500

        self.vectorize_layer = layers.TextVectorization(
        standardize=self.custom_standardization,
        max_tokens=max_features,
        output_mode="int",
        output_sequence_length=sequence_length,
        )


        (self.raw_train_ds, self.raw_test_ds, self.text_ds) = data

        self.vectorize_layer.adapt(self.text_ds)

    
        self.train_ds = self.raw_train_ds.map(self.vectorize_text)
        self.test_ds = self.raw_test_ds.map(self.vectorize_text)


    

        inlayer = Input(shape=(None,), dtype="int64")

        aux_layer = layers.Embedding(max_features, embedding_dim)(inlayer)
        aux_layer = layers.Dropout(0.5)(aux_layer)

        aux_layer = layers.Conv1D(128, 7, padding="valid", activation="relu", strides=3)(aux_layer)
        aux_layer = layers.Conv1D(128, 7, padding="valid", activation="relu", strides=3)(aux_layer)
        aux_layer = layers.GlobalMaxPooling1D()(aux_layer)


        aux_layer = layers.Dense(128, activation="relu")(aux_layer)
        aux_layer = layers.Dropout(0.5)(aux_layer)

                
        if "num_inputs" in config.keys():
            self.num_inputs = (int(config['num_inputs']), )
        if "layers_dict" in config.keys():
            self.layers_dict = config['layers_dict'] 
        dict_keys = [str(key) for key in self.layers_dict.keys()]
        dict_keys.sort()
        for key in dict_keys:
                    aux_layer = Dense(int(
                    self.layers_dict[key]['num_neurons']), self.layers_dict[key]["activation"])(aux_layer)
        
        self.model = Model(inputs=inlayer, outputs=aux_layer)


    def train_special(self):
            
        self.model.compile(loss="binary_crossentropy", optimizer="adam", metrics=["accuracy"])

        epochs = 3


        self.model.fit(self.train_ds, validation_data=self.test_ds, epochs=epochs)

