'''This file defines the ProcessText Class'''

from ProcessData import ProcessData
from .ProcessData import ProcessError
import pyarrow.parquet as pq
import pandas as pd
import numpy as np
from keras.api.utils import text_dataset_from_directory

class ProcessText(ProcessData):

    """This class will process the text input data before its sended to the
      neural network. It inherits from ProcessData
    """

    def process_dir(self, dir_name):
        """Process the directory depending if its for test or train

        Args:
        dir_name (str)

        Returns:
            None
        """
        if "train" in dir_name[-6:]:
            self.process_train_file(dir_name)
        if "test" in dir_name[-6:]:
            self.process_test_file(dir_name)

    def process_test_file(self, file_name):
        """Process the data from a test file

        Args:
        file_name (str): path to the file

        Returns:
            None
        """
        array_x: np.ndarray
        array_y: np.ndarray
        batch_size = 32


        self.raw_test_ds = text_dataset_from_directory(
                        directory=file_name,label_mode="categorical",
                        batch_size=batch_size,  labels='inferred')


    def process_train_file(self, file_name):
        """Process the data from a train file

        Args:
        file_name (str): path to the file

        Returns:
            None
        """
        array_x: np.ndarray
        array_y: np.ndarray
        batch_size = 32

        array_x, array_y = self.x_train, self.y_train
        self.raw_train_ds = text_dataset_from_directory(
                        directory=file_name,label_mode="categorical",
                        batch_size=batch_size,
                        validation_split=0.2,
                        subset="training", seed=1337, labels='inferred')




    def reshape_data(self, num_outputs):

        text_ds = self.raw_train_ds.map(lambda x, y: x)

        self.data_processed = (self.raw_train_ds, self.raw_test_ds, text_ds)