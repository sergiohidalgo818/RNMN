'''This file defines the ProcessText Class'''

from typing import Tuple
import numpy as np
from ProcessData import ProcessData

class ProcessText(ProcessData):

    """This class enherits from ProcessData and will process the text
      data before its sended to the neural network

    Atrs:
        data_filename (str): The file location of the data
        data_processed (Tuple(np.array, np.array)): Processed data, 
            a tuple with entries and outputs
    """
    data_filename : str
    data_processed : Tuple

    def process(self):
        """Process the data from a file or set of files

        Args:
        None

        Returns:
            None
        """
        pass