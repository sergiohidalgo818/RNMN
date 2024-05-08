'''This file defines the ProcessData Class'''

import numpy as np
from keras.api.utils import to_categorical
import os


class ProcessError(Exception):
    '''Raised when there is an error during a file processing'''

    def __init__(self, message, *args):
        self.message = message
        super(ProcessError, self).__init__(message, *args)


class ProcessData():

    """This class will process the input data before its sended to the
      neural network

    Atrs:
        data_directory (str): The file location of the data files
        data_processed (tuple(np.array, np.array)): Processed data, 
            a tuple with entries and outputs, that are stored in the
              following way -> tuple(entries[line][atribute], outputs[line][class])
    """
    data_directory: str
    data_train_processed: tuple
    data_test_processed: tuple
    input_size: int

    def __init__(self, data_directory) -> None:
        """Initializes the ProcessedData class

        Args:
        data_directory (str): The directory location of the data

        Returns:
            None
        """
        if os.path.exists(data_directory):
            self.data_directory = data_directory
        else:
            raise ProcessError("Directory does not exist")

        (self.x_train, self.y_train) = (np.array([]), np.array([]))
        (self.x_test, self.y_test) = (np.array([]), np.array([]))
        self.data_processed = (
            (self.x_train, self.y_train), (self.x_test, self.y_test))

    def process(self):
        """Process the data from a set of files on a directory

        Args:
        None

        Returns:
            None
        """

        list_of_files = os.listdir(self.data_directory)

        if "train" not in list_of_files or "test" not in list_of_files:
            raise ProcessError("Folder doesnt contains 'test' or 'train' data")

        if len(list_of_files) == 0:
            raise ProcessError("Directory empty")

        for file in list_of_files:
            dir_name = os.path.join(self.data_directory, file)
            try:
                self.process_dir(dir_name)
            except ProcessError:
                raise ProcessError("File not compatible")

    def process_dir(self, dir_name):
        """Process the directory depending if its for test or train

        Args:
        dir_name (str)

        Returns:
            None
        """
        list_of_files = os.listdir(dir_name)

        if len(list_of_files) == 0:
            raise ProcessError("Directory empty")

        for file in list_of_files:
            file_name = os.path.join(dir_name, file)
            try:

                if "train" in dir_name[-6:]:
                    self.process_train_file(file_name)
                elif "test" in dir_name[-6:]:
                    self.process_test_file(file_name)

            except ProcessError:
                raise ProcessError("File not compatible")
            else:
                self.data_processed = (
                    (self.x_train, self.y_train), (self.x_test, self.y_test))

    def process_train_file(self, file_name):
        """Process the data from a file for train

        Args:
        file_name (str): path to the file

        Returns:
            None
        """
        pass

    def process_test_file(self, file_name):
        """Process the data from a file for train

        Args:
        file_name (str): path to the file

        Returns:
            None
        """
        pass

    def bin_array(self, x: str, len_of_arr: int) -> np.ndarray:
        """Transforms a string of binary string to a numpy array

        Args:
        x (str): binary string
        len_of_arr (int): length of the final array

        Returns:
            The numpy array
        """
        num_list = [int(char) for char in x]

        tam = len(num_list)

        while tam <= len_of_arr:
            num_list = [0] + num_list
            tam += 1

        return np.array(num_list)

    def np_assign(self, x) -> np.ndarray:
        """Assigns 1 to an index on a array of 0s

            Args:
            x (int): index of the value

            Returns:
                The numpy array
        """
        np_array = np.zeros((10,), dtype=int)
        np_array[x] = 1
        return np_array

    def reshape_data(self, num_outputs):
        pass
