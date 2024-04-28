'''This file defines the ProcessImage Class'''

from ProcessData import ProcessData

class ProcessImage(ProcessData):

    """This class will process the image input data before its sended to the
      neural network. It inherits from ProcessData
    """

    def process_file(self, file_name):
        """Process the data from a image

        Args:
        file_name (str): path to the file

        Returns:
            None
        """
        pass
