'''This file defines the RNMNModel Class'''

from RNMNAbstract import RNMNAbstract
from RNMNSmall import RNMNTextModel
import numpy as np

class RNMNModel(RNMNAbstract):
    """The RNMNModel class will create the big Model for a given
      datasets or load a previous one
    """

    _processed_data_and_types : dict

    def __init__(self, processed_data_and_types:dict) -> None:
        self._processed_data_and_types = processed_data_and_types


    def create_neural_model():
        pass

    def load_neural_model(directory: str):
        pass

    def _create_audio_model(audio_data: np.ndarray):
        pass

    def _create_text_model(audio_data: np.ndarray):
        
        pass

    def _create_image_model(audio_data: np.ndarray):
        pass

    def predict() -> int:
        pass

    def train():
        pass