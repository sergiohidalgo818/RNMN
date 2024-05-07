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




    def transform_txt_deprecated(self, file_name):
        """Transforms a txt file to data

        Returns:
            None
        """
        array_x, array_y = self.data_processed

        f = open(file_name, "r")

        data = f.read()

        data_list = list()

        flag_add = False

        while len(data) % int(self.input_size/8) != 0:
            data = " " + data
            flag_add = True

        if flag_add:
            data = " " + data

        last = 0
        for block in range(int(self.input_size/8), len(data), int(self.input_size/8)):
            word = data[last:block]

            transformed = ''.join('{0:08b}'.format(ord(x), 'b') for x in word)

            data_list.append(self.bin_array(
                transformed, int(self.input_size/8)))
            last = block

        if array_x.size == 0:
            array_x = np.stack(data_list, axis=0)
        else:
            array_x = np.append(array_x, np.array(data_list), axis=0)

        self.data_processed = (array_x, None)

    def process_file_deprecated(self, file_name):
        """Process the data from a file

        Args:
        file_name (str): path to the file
        data_tuple (tuple): tuple with the data

        Returns:
            None
        """

        if file_name[-4:] == '.txt':
            self.transform_txt(file_name)

        elif file_name[-8:] == '.parquet':

            array_x: np.ndarray
            array_y: np.ndarray

            array_x, array_y = data_tuple

            table = pq.read_table(file_name)
            data_frame: pd.DataFrame = table.to_pandas()

            x = data_frame.iloc[:, :-10]
            y = data_frame.iloc[:, -10:]

            if array_x.size == 0:
                array_x = x.to_numpy()
            else:
                array_x = np.append(array_x, x.to_numpy(), axis=0)

            if array_y.size == 0:
                array_y = y.to_numpy()
            else:
                array_y = np.append(array_y, y.to_numpy(), axis=0)

            data_tuple = (array_x, array_y)

        else:
            raise ProcessError("Error on file format")
        

    def reshape_data(self, num_outputs):

        text_ds = self.raw_train_ds.map(lambda x, y: x)

        self.data_processed = (self.raw_train_ds, self.raw_test_ds, text_ds)