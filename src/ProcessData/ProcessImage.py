'''This file defines the ProcessImage Class'''

from ProcessData import ProcessData
from .ProcessData import ProcessError
import binascii
import numpy as np
import os
import idx2numpy


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
