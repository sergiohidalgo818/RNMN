'''This file defines the InputType Enum'''

from enum import Enum



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
    
