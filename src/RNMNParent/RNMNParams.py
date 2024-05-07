'''This file defines the InputType Enum'''

from enum import Enum
from keras import metrics


class RNMNMetricsTraduction(Enum):

    
    ACCURACY = (metrics.Accuracy(name='accuracy'), "Accuracy")

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

    ACCURACY_NAME = "accuracy"

    TP_NAME = "true_positives"
    
    FP_NAME = "false_positives"

    TN_NAME = "true_negatives"

    FN_NAME = "false_negatives"

    ACC_NAME = "binary_accuracy"

    P_NAME = "precision"

    R_NAME = "recall"

    AUC_NAME = "auc"





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
    
