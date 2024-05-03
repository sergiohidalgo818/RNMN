'''This file defines the RNMNModel Class'''

from RNMNParent import RNMNParent
from keras import optimizers, losses
from .RNMNSmall import RNMNAudioModel, RNMNImageModel, RNMNTextModel
from RNMNApp import InputType
from sklearn.model_selection import train_test_split


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

    _models: set

    def __init__(self, **kwargs) -> None:

        self._models = set()

        self.text_config = dict()
        self.audio_config = dict()
        self.image_config = dict()

        if "params_dict" in kwargs.keys():
            if "text_config" in kwargs["params_dict"].keys():
                self.text_config = kwargs["params_dict"]['text_config']
                self._create_text_model()
            if "audio_config" in kwargs["params_dict"].keys():
                self.audio_config = kwargs["params_dict"]['audio_config']
                self._create_audio_model()
            if "image_config" in kwargs["params_dict"].keys():
                self.image_config = kwargs["params_dict"]['image_config']
                self._create_image_model()

    def compile_model(self, parameters):
        
        if "optimizer" in parameters.keys():
            optimizer = parameters['optimizer']
        if "loss" in parameters.keys():
            loss = parameters['loss']
        if "metrics" in parameters.keys():
            metrics = parameters['metrics']




    def _create_text_model(self):
        self.text_model = RNMNTextModel(self.text_config)
        self._models.add("text")

    def _create_audio_model(self):
        self.audio_model = RNMNAudioModel(self.audio_config)
        self._models.add("audio")

    def _create_image_model(self):
        self.image_model = RNMNImageModel(self.image_config)
        self._models.add("image")


    def add_data_text_model(self, text_data: tuple):
        self.text_model.add_data_to_model(text_data[0], text_data[1])

    def add_data_audio_model(self, audio_data: tuple):
        self.audio_model.add_data_to_model(audio_data[0], audio_data[1])

    def add_data_image_model(self, image_data: tuple):
        self.image_model.add_data_to_model(image_data[0], image_data[1])

    def predict(self) -> int:
        self.model

    def train(self, config_train: dict):
        x_train, x_rest, y_train, y_rest = train_test_split(
            self.text_model.data_x, self.text_model.data_y, test_size=0.4)
        x_val, x_test, y_val, y_test = train_test_split(
            self.text_model.data_x, self.text_model.data_y, test_size=0.5)
        history = self.model.fit(
            x_train, y_train, epochs=config_train['epochs'], verbose=config_train['verbose'], validation_data=(x_val, y_val))

        print(history)
