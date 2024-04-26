'''This file defines the ProcessData Class'''

from typing import Tuple

class ProcessData():

    """This class will process the input data before its sended to the
      neural network

    Atrs:
        data_filename (str): The file location of the data
        data_processed (Tuple(np.array, np.array)): Processed data, 
            a tuple with entries and outputs
    """
    data_filename : str
    data_processed : Tuple

    def __init__(self, data_filename) -> None:
        """Initializes the ProcessedData class

        Args:
        data_filename (str): The file location of the data

        Returns:
            None
        """
        self.data_filename = data_filename


    def process(self):
        """Process the data from a file or set of files

        Args:
        None

        Returns:
            None
        """
        pass