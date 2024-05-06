'''This file defines the ProcessImage Class'''

from ProcessData import ProcessData
from .ProcessData import ProcessError
import binascii
import numpy as np
import os
import idx2numpy
from keras.api.utils import to_categorical


class ProcessImage(ProcessData):

    """This class will process the image input data before its sended to the
      neural network. It inherits from ProcessData
    """

    def process_test_file(self, file_name):
        """Process the data from a test file

        Args:
        file_name (str): path to the file

        Returns:
            None
        """
        array_x: np.ndarray
        array_y: np.ndarray

        array_x, array_y = (self.x_test, self.y_test)

        readed_array = idx2numpy.convert_from_file(file_name)

        if "label" in file_name:

            if array_y.size == 0:
                array_y = np.array(readed_array)

            else:
                array_y = np.append(array_y, np.array(readed_array), axis=0)

        else:
            if array_x.size == 0:
                array_x = np.array(readed_array)

            else:
                array_x = np.append(array_x, np.array(readed_array), axis=0)

        (self.x_test, self.y_test) = (array_x, array_y)

    def process_train_file(self, file_name):
        """Process the data from a train file

        Args:
        file_name (str): path to the file

        Returns:
            None
        """
        array_x: np.ndarray
        array_y: np.ndarray

        array_x, array_y = self.x_train, self.y_train

        readed_array = idx2numpy.convert_from_file(file_name)

        if "label" in file_name:

            if array_y.size == 0:
                array_y = np.array(readed_array)

            else:
                array_y = np.append(array_y, np.array(readed_array), axis=0)

        else:
            if array_x.size == 0:
                array_x = np.array(readed_array)

            else:
                array_x = np.append(array_x, np.array(readed_array), axis=0)

        (self.x_train, self.y_train) = (array_x, array_y)


    def reshape_data(self, num_outputs):
        self.x_train = np.reshape(
            self.x_train, np.append(self.x_train.shape, (1)))
        self.x_test = np.reshape(
            self.x_test, np.append(self.x_test.shape, (1)))

        self.x_train = self.x_train.astype('float32')
        self.x_test = self.x_test.astype('float32')
        self.x_train = self.x_train / 255
        self.x_test = self.x_test / 255

        self.y_train = to_categorical(self.y_train, num_outputs)
        self.y_test = to_categorical(self.y_test, num_outputs)

        self.data_processed = (
            (self.x_train, self.y_train), (self.x_test, self.y_test))