'''This file defines the InputType Enum'''

from enum import Enum
from keras import layers


class ParamError(Exception):
    '''Raised when there is an error during a lecture of params'''

    def __init__(self, message, *args):
        self.message = message
        super(ParamError, self).__init__(message, *args)


class RNMNMetrics(Enum):
    '''This enum is for the type of metrics'''

    ACCURACY = "accuracy"

    TP = "true_positives"

    FP = "false_positives"

    TN = "true_negatives"

    FN = "false_negatives"

    ACC = "binary_accuracy"

    P = "precision"

    R = "recall"

    AUC = "auc"


class RNMNOptimizers(Enum):
    '''This enum is for the type of optimizers'''

    ADAM = "adam"

    SGD = "SGD"

    RMSprop = "rmsprop"

    ADAMW = "adamw"

    ADADELTA = "adadelta"

    ADAGRAD = "adagrad"

    ADAMAX = "adamax"

    ADAFACTOR = "adafactor"

    NADAM = "nadam"

    FTRL = "ftrl"

    LION = "lion"


class RNMNLosses(Enum):
    '''This enum is for the type of losses'''

    CATT_CROSS = "categorical_crossentropy"

    BINARY_CROSS = "binary_crossentropy"

    MSE = "mse"


class RNMNActivations(Enum):
    '''This enum is for the type of activations'''

    RELU = "relu"

    SIGMOID = "sigmoid"

    SOFTMAX = "softmax"

    SOFTPLUS = "softplus"


class RNMNLayers(Enum):
    '''This enum is for the type of layers'''

    DENSE = "Dense"
    EMMBEDING = "Embedding"
    DROPOUT = "Dropout"
    CONV1D = "Conv1D"
    GLOBMAXPOOL1D = "GlobalMaxPooling1D"
    CONV2D = "Conv2D"
    MAXPOOL2D = "MaxPooling2D"
    FLATTEN = "Flatten"

    def default_app_layers_values():
        '''Might use it later
        '''
        default_layers = dict()
        default_layers[RNMNLayers.DENSE] = dict()
        default_layers[RNMNLayers.DENSE]['fun'] = layers.Dense
        default_layers[RNMNLayers.DENSE]['params'] = dict()
        default_layers[RNMNLayers.DENSE]['params']['units'] = 128
        default_layers[RNMNLayers.DENSE]['params']['activation'] = "relu"

        default_layers[RNMNLayers.EMMBEDING] = dict()
        default_layers[RNMNLayers.EMMBEDING]['fun'] = layers.Embedding
        default_layers[RNMNLayers.EMMBEDING]['params'] = dict()
        default_layers[RNMNLayers.EMMBEDING]['params']['input_dim'] = 20000
        default_layers[RNMNLayers.EMMBEDING]['params']['output_dim'] = 128

        default_layers[RNMNLayers.DROPOUT] = dict()
        default_layers[RNMNLayers.DROPOUT]['fun'] = layers.Dropout
        default_layers[RNMNLayers.DROPOUT]['params'] = dict()
        default_layers[RNMNLayers.DROPOUT]['params']['rate'] = 0.5

        default_layers[RNMNLayers.CONV1D] = dict()
        default_layers[RNMNLayers.CONV1D]['fun'] = layers.Conv1D
        default_layers[RNMNLayers.CONV1D]['params'] = dict()
        default_layers[RNMNLayers.CONV1D]['params']['filters'] = 128
        default_layers[RNMNLayers.CONV1D]['params']['kernel_size'] = 7
        default_layers[RNMNLayers.CONV1D]['params']['strides'] = 3
        default_layers[RNMNLayers.CONV1D]['params']['padding'] = "valid"
        default_layers[RNMNLayers.CONV1D]['params']['activation'] = "relu"

        default_layers[RNMNLayers.GLOBMAXPOOL1D] = dict()
        default_layers[RNMNLayers.GLOBMAXPOOL1D]['fun'] = layers.GlobalMaxPooling1D
        default_layers[RNMNLayers.GLOBMAXPOOL1D]['params'] = dict()

        default_layers[RNMNLayers.CONV2D] = dict()
        default_layers[RNMNLayers.CONV2D]['fun'] = layers.Conv2D
        default_layers[RNMNLayers.CONV2D]['params'] = dict()
        default_layers[RNMNLayers.CONV2D]['params']['filters'] = 32
        default_layers[RNMNLayers.CONV2D]['params']['kernel_size'] = 5
        default_layers[RNMNLayers.CONV2D]['params']['strides'] = (1, 1)
        default_layers[RNMNLayers.CONV2D]['params']['padding'] = "same"
        default_layers[RNMNLayers.CONV2D]['params']['activation'] = "relu"

        default_layers[RNMNLayers.MAXPOOL2D] = dict()
        default_layers[RNMNLayers.MAXPOOL2D]['fun'] = layers.MaxPooling2D
        default_layers[RNMNLayers.MAXPOOL2D]['params'] = dict()

        default_layers[RNMNLayers.FLATTEN] = dict()
        default_layers[RNMNLayers.FLATTEN]['fun'] = layers.Flatten
        default_layers[RNMNLayers.FLATTEN]['params'] = dict()

        return default_layers

    def gen_options_layers():
        '''Generate a dict to help translating the layers
        '''
        options_layers = dict()

        options_layers[RNMNLayers.DENSE] = layers.Dense

        options_layers[RNMNLayers.EMMBEDING] = layers.Embedding

        options_layers[RNMNLayers.DROPOUT] = layers.Dropout

        options_layers[RNMNLayers.CONV1D] = layers.Conv1D

        options_layers[RNMNLayers.GLOBMAXPOOL1D] = layers.GlobalMaxPool1D

        options_layers[RNMNLayers.CONV2D] = layers.Conv2D

        options_layers[RNMNLayers.MAXPOOL2D] = layers.MaxPooling2D

        options_layers[RNMNLayers.FLATTEN] = layers.Flatten

        return options_layers
