'''This file defines the InputType Enum'''

from enum import Enum
from keras import metrics


class RNMNMetricsTraduction(Enum):
    TP = (metrics.TruePositives(name='TP'), "True Positives")

    FP = (metrics.FalsePositives(name='FP'), "False Positives")

    TN = (metrics.TrueNegatives(name='TN'), "True Negatives")

    FN = (metrics.FalseNegatives(name='FN'), "False Negatives")

    ACC = (metrics.BinaryAccuracy(name='ACC'), "Binary Accuracy")

    P = (metrics.Precision(name='P'), "Precision")

    R = (metrics.Recall(name='R'), "Recall")

    AUC = (metrics.AUC(name='AUC'), "AUC")

    def translate(metrics_list:list)->list:
        final_list = list()
        for m in metrics_list:
            for t in RNMNMetricsTraduction:
                if t.value[1] == m:
                    final_list.append(t.value[0])
                    break                
        return final_list


class RNMNMetrics(Enum):
    '''This enum is for the type of metrics'''

    TP_NAME = "True Positives"

    FP_NAME = "False Positives"

    TN_NAME = "True Negatives"

    FN_NAME = "False Negatives"

    ACC_NAME = "Binary Accuracy"

    P_NAME = "Precision"

    R_NAME = "Recall"

    AUC_NAME = "AUC"



class RNMNOptimizers(Enum):
    '''This enum is for the type of optimizers'''

    SGD = "SGD"

    ADAM = "adam"

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

    BINARY_CROSS = "binary_crossentropy"

    MSE = "mse"

class RNMNActivations(Enum):
    '''This enum is for the type of losses'''

    RELU = "relu"

    SIGMOID = "sigmoid"

    SOFTMAX = "softmax"
    
    SOFTPLUS = "softplus"
    
