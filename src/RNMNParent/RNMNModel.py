'''This file defines the RNMNModel Class'''

from RNMNParent import RNMNParent
from keras import optimizers, losses, Model, layers
from .RNMNSmall import RNMNAudioModel, RNMNImageModel, RNMNTextModel
from RNMNApp import InputType
from sklearn.model_selection import train_test_split
import numpy as np


class RNMNModel(RNMNParent):
    """The RNMNModel class will create the big Model for a given
      datasets or load a previous one
    """

    text_config: dict
    audio_config: dict
    image_config: dict

    text_model: RNMNTextModel
    audio_model: RNMNAudioModel
    image_model: RNMNImageModel
    
    x_train : list
    y_train : list
    x_test : list
    y_test : list


    def __init__(self, **kwargs) -> None:


        self.text_config = dict()
        self.audio_config = dict()
        self.image_config = dict()

        models_in = list()
        models_out  = list()
        
        self.x_train = list()
        self.y_train = list()
        self.x_test  = list()
        self.y_test  = list()

        

        if "params_dict" in kwargs.keys():
            if "text_config" in kwargs["params_dict"].keys():
                self.text_config = kwargs["params_dict"]['text_config']
                
                self._create_text_model(kwargs["data_and_types"][InputType.TEXT])
                models_in.append(self.text_model.model.input)
                models_out.append(self.text_model.model.output)

                self.x_train.append(self.text_model.x_train)
                self.y_train.append(self.text_model.y_train)
                self.x_test.append(self.text_model.x_test)
                self.y_test.append(self.text_model.y_test)

            if "audio_config" in kwargs["params_dict"].keys():
                self.audio_config = kwargs["params_dict"]['audio_config']
                self._create_audio_model(kwargs["data_and_types"][InputType.AUDIO])
                models_in.append(self.audio_model.model.input)
                models_out.append(self.audio_model.model.output)

                self.x_train.append(self.audio_model.x_train)
                self.y_train.append(self.audio_model.y_train)
                self.x_test.append(self.audio_model.x_test)
                self.y_test.append(self.audio_model.y_test)

            if "image_config" in kwargs["params_dict"].keys():
                self.image_config = kwargs["params_dict"]['image_config']
                self._create_image_model(kwargs["data_and_types"][InputType.IMAGE])
                models_in.append(self.image_model.model.input)
                models_out.append(self.image_model.model.output)

                self.x_train.append(self.image_model.x_train)
                self.y_train.append(self.image_model.y_train)
                self.x_test.append(self.image_model.x_test)
                self.y_test.append(self.image_model.y_test)

            outputs = layers.concatenate(models_out)

            self.model = Model(inputs=models_in, outputs=outputs)

            

    def compile_model(self, parameters):
        
        optimizer = parameters['optimizer']
        loss = parameters['loss']
        metrics = parameters['metrics']
        self.model.compile(optimizer=optimizer, loss=loss, metrics=metrics)


    def _create_text_model(self, data):
        self.text_model = RNMNTextModel(data, self.text_config)

    def _create_audio_model(self, data):
        self.audio_model = RNMNAudioModel(data, self.audio_config)

    def _create_image_model(self, data):
        self.image_model = RNMNImageModel(data, self.image_config)

    def add_data_text_model(self, text_data: tuple):
        self.text_model.add_data_to_model(text_data)

    def add_data_audio_model(self, audio_data: tuple):
        self.audio_model.add_data_to_model(audio_data)

    def add_data_image_model(self, image_data: tuple):
        self.image_model.add_data_to_model(image_data)

    def predict(self, data):
        return self.model.predict(data)

    def train(self, config_train: dict):
        history = self.model.fit(self.x_train, self.image_model.y_train, batch_size=16, epochs=config_train['epochs'], validation_data=(self.image_model.x_test, self.image_model.y_test), shuffle=True)

        self.model.summary()

