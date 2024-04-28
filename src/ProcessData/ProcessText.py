'''This file defines the ProcessText Class'''

from ProcessData import ProcessData
import pyarrow.parquet as pq
import pandas as pd
import numpy as np

class ProcessText(ProcessData):

    """This class will process the text input data before its sended to the
      neural network. It inherits from ProcessData
    """

    def process_file(self, file_name):
        """Process the data from a text file

        Args:
        file_name (str): path to the file

        Returns:
            None
        """

        array_x : np.ndarray
        array_y : np.ndarray
        
        array_x, array_y = self.data_processed

        
        table = pq.read_table(file_name)
        data_frame:pd.DataFrame = table.to_pandas()
      
        x = data_frame.iloc[:,:-10]
        y = data_frame.iloc[:,-10:]


        if array_x.size == 0:
          array_x = x.to_numpy()
        else:
           array_x=np.append(array_x, x.to_numpy(), axis=0)


        if array_y.size == 0:
          array_y = y.to_numpy()
        else:
           array_y= np.append(array_y, y.to_numpy(), axis=0)


        self.data_processed = (array_x, array_y)