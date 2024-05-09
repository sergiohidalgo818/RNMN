'''This file defines the RNMNImageModel Class'''

from .RNMNSmall import RNMNSmall
from keras import Input


class RNMNImageModel(RNMNSmall):
    """Class of the image model
    """

    def __init__(self, data, config) -> None:
        """Initializes the model by calling the
          parent class
        """
        (self.x_train, self.y_train), (self.x_test, self.y_test) = data

        self.in_layer = Input(shape=self.x_train.shape[
            1:])

        if "num_inputs" in config.keys():
            self.num_inputs = (int(config['num_inputs']), )
        if "layers_dict" in config.keys():
            self.layers_dict = config['layers_dict']

        super().__init__()
