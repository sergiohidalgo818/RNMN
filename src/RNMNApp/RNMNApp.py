'''This file defines the RNMNApp Class'''

import pickle
import os
from .RNMNGuiApp import RNMNAppGui
from .InputType import InputType, ImportError
from ProcessData import ProcessData, ProcessError
from ProcessData import ProcessText
from RNMNParent import RNMNModel


class RNMNApp():
    """This class start the app and get the location of the data and
      the trained model (if it exists) 
    """

    preprocessed_data_and_types: dict
    processed_data_and_types: dict
    model: RNMNModel
    app_gui: RNMNAppGui
    _no_gui: bool

    _has_model : bool

    def __init__(self,**kwargs) -> None:
        self.preprocessed_data_and_types = dict()
        self._no_gui = kwargs['gui']
        self._has_model = False

    def start_app(self):
        if self._no_gui == False:
            self.app_gui_start()
        else:
            self.app_no_gui_start()

    def get_text_data(self, directory: str):

        try:
            text = ProcessText(directory)
        except ProcessError as ex:
            raise ImportError("Error while importing text data")

        self.preprocessed_data_and_types[InputType.TEXT] = text

    def get_audio_data(self, directory: str):

        try:
            audio = ProcessData(directory)
        except ProcessError as ex:
            raise ImportError("Error while importing audio data")

        self.preprocessed_data_and_types[InputType.AUDIO] = audio

    def get_image_data(self, directory: str):

        try:
            image = ProcessData(directory)
        except ProcessError as ex:
            raise ImportError("Error while importing image data")

        self.preprocessed_data_and_types[InputType.IMAGE] = image

    def del_text_data(self):
        del self.processed_data_and_types[InputType.TEXT]
        del self.preprocessed_data_and_types[InputType.TEXT]

    def del_audio_data(self):
        del self.processed_data_and_types[InputType.AUDIO]
        del self.preprocessed_data_and_types[InputType.AUDIO]

    def del_image_data(self):
        del self.processed_data_and_types[InputType.IMAGE]
        del self.preprocessed_data_and_types[InputType.IMAGE]

    def create_model(self, params_dict):
        self.model = RNMNModel(params_dict)
        self._has_model = True


    def save_model(self, directory: str):
        with open(directory, 'wb') as output:
            pickle.dump(self.model, output, pickle.HIGHEST_PROTOCOL)

    def load_model(self, directory: str):
        with open(directory, 'rb') as input:
            try:
                self.model = pickle.load(input)
            except pickle.UnpicklingError as ex:
                raise ImportError("Error while importing model")
            else:
                self._has_model = True


    def preprocess_typedata_data(self, list_types):
        self.processed_data_and_types = dict()

        for k in list_types:
            try:
                self.preprocessed_data_and_types[k].process()
            except ProcessError:
                raise ImportError("Error on process data")
            else:
                self.processed_data_and_types[k] = self.preprocessed_data_and_types[k].data_processed

    def preprocess_all_data(self):
        self.processed_data_and_types = dict()

        for k in self.preprocessed_data_and_types.keys():

            try:
                self.preprocessed_data_and_types[k].process()
            except ProcessError:
                raise ImportError("Error on process data")
            else:
                self.processed_data_and_types[k] = self.preprocessed_data_and_types[k].data_processed

    def app_no_gui_start(self):
        pass

    def app_gui_start(self):
        self.app_gui = RNMNAppGui(self)

        self.app_gui.mainloop()
