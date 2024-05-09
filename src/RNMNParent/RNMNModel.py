'''This file defines the RNMNModel Class'''

from RNMNParent import RNMNParent
from keras import Model, layers
from .RNMNSmall import RNMNAudioModel, RNMNImageModel, RNMNTextModel
from RNMNApp import InputType
from keras import layers
import keras


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

    x_train: list
    y_train: list
    x_test: list
    y_test: list

    history: list
    models: list

    def __init__(self, **kwargs) -> None:
        """Big model class with all the models
        """

        self.text_config = dict()
        self.audio_config = dict()
        self.image_config = dict()

        self.models_in = list()
        self.models_out = list()

        self.models = list()

        self.history = list()

        if "params_dict" in kwargs.keys():
            if "text_config" in kwargs["params_dict"].keys():
                self.text_config = kwargs["params_dict"]['text_config']
                self._create_text_model(
                    kwargs["data_and_types"][InputType.TEXT])
                self.models.append(InputType.TEXT)

            if "audio_config" in kwargs["params_dict"].keys():
                self.audio_config = kwargs["params_dict"]['audio_config']
                self._create_audio_model(
                    kwargs["data_and_types"][InputType.AUDIO])
                self.models.append(InputType.AUDIO)

            if "image_config" in kwargs["params_dict"].keys():
                self.image_config = kwargs["params_dict"]['image_config']
                self._create_image_model(
                    kwargs["data_and_types"][InputType.IMAGE])
                self.models.append(InputType.IMAGE)

    def compile_model(self, parameters, model):
        """Compiles the models 

            Args:
            parameters (dict): dictionary with values

            Returns:
                None
        """

        optimizer = parameters['optimizer']
        loss = parameters['loss']
        metrics = parameters['metrics']

        if "texto" in model:
            self.text_model.model.compile(
                optimizer=optimizer, loss=loss, metrics=metrics)

        if "imagen" in model:
            self.image_model.model.compile(
                optimizer=optimizer, loss=loss, metrics=metrics)

        if "audio" in model:
            self.audio_model.model.compile(
                optimizer=optimizer, loss=loss, metrics=metrics)

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
        return self.model.predict(data, verbose=0)

    def train(self, config_train: dict, model):
        """Trains the models and fuse them

            Args:
            config_train (dict): dictionary with the train config

            Returns:
                None
        """

        if "texto" == model:
            hist = self.text_model.model.fit(
                self.text_model.train_ds, validation_data=self.text_model.test_ds, epochs=config_train['epochs'])
            self.history.append(hist)

            in_layer = layers.Input(shape=(1,), dtype="string")

            index = self.text_model.vectorize_layer(in_layer)

            outputs = self.text_model.model(index)
            text_model = keras.Model(in_layer, outputs)
            text_model.compile(
                loss="binary_crossentropy", optimizer="adam", metrics=["accuracy"]
            )

            self.models_in.append(text_model.input)
            self.models_out.append(text_model.output)

        if "imagen" == model:
            hist = self.image_model.model.fit(self.image_model.x_train, self.image_model.y_train, batch_size=16,
                                              epochs=config_train['epochs'], validation_data=(self.image_model.x_test, self.image_model.y_test), shuffle=True)
            self.models_in.append(self.image_model.model.input)
            self.models_out.append(self.image_model.model.output)
            self.history.append(hist)

        if "audio" == model:
            hist = self.audio_model.model.fit(
                self.text_model.train_ds, validation_data=self.text_model.test_ds, epochs=config_train['epochs'])
            self.models_in.append(self.audio_model.model.input)
            self.models_out.append(self.audio_model.model.output)
            self.history.append(hist)

    def fuse_model(self):
        outputs = keras.layers.concatenate(
            self.models_out, name="concatenated_layer")

        self.model = Model(inputs=self.models_in, outputs=[outputs])

        self.model.compile(loss="binary_crossentropy",
                           optimizer="adam", metrics=["accuracy"])

        self.models_in = list()
        self.models_out = list()
