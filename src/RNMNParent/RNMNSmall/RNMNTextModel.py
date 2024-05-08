'''This file defines the RNMNTextModel Class'''

from .RNMNSmall import RNMNSmall
from keras import Input, layers
import tensorflow
import re
import string


class RNMNTextModel(RNMNSmall):
    """Class of the text model
    """

    @tensorflow.keras.utils.register_keras_serializable()
    def vectorize_text(self, text, label):
        text = tensorflow.expand_dims(text, -1)
        return self.vectorize_layer(text), label

    @tensorflow.keras.utils.register_keras_serializable()
    def custom_standardization(input_data):
        lowercase = tensorflow.strings.lower(input_data)
        return tensorflow.strings.regex_replace(
            lowercase, f"[{re.escape(string.punctuation)}]", ""
        )
    max_features = 20000
    sequence_length = 500

    vectorize_layer = layers.TextVectorization(
        standardize=custom_standardization,
        max_tokens=max_features,
        output_mode="int",
        output_sequence_length=sequence_length,
    )

    def __init__(self,  data,  config) -> None:
        """Initializes the model by calling the
          parent class and maping the text to integers
            for the training data
        """
        self.in_layer = Input(shape=(None,), dtype="int64")

        if "num_inputs" in config.keys():
            self.num_inputs = (int(config['num_inputs']), )
        if "layers_dict" in config.keys():
            self.layers_dict = config['layers_dict']

        super().__init__()

        self.vectorize_layer

        (self.raw_train_ds, self.raw_test_ds, self.text_ds) = data

        self.vectorize_layer.adapt(self.text_ds)

        self.train_ds = self.raw_train_ds.map(self.vectorize_text)
        self.test_ds = self.raw_test_ds.map(self.vectorize_text)
