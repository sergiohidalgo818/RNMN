'''This file defines the ProcessData Class'''

from typing import Tuple
import numpy as np
import os

class ProcessData():

    """This class will process the input data before its sended to the
      neural network

    Atrs:
        data_directory (str): The file location of the data files
        data_processed (Tuple(np.array, np.array)): Processed data, 
            a tuple with entries and outputs
    """
    data_directory: str
    data_processed: Tuple

    def __init__(self, data_directory) -> None:
        """Initializes the ProcessedData class

        Args:
        data_directory (str): The directory location of the data

        Returns:
            None
        """
        self.data_directory = data_directory
        self.data_processed = Tuple(np.array(), np.array())

    def process(self):
        """Process the data from a set of files

        Args:
        None

        Returns:
            None
        """
        list_of_files = os.listdir(self.data_directory)

        for file in list_of_files:
            file_name = os.path.join(self.data_directory, file)
            if os.path.isfile(file_name):
                self.process_file(file_name)

    def process_file(self, file_name):
        """Process the data from a file or set of files

        Args:
        None

        Returns:
            None
        """
        pass
