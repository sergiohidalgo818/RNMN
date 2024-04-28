'''This file defines the ProcessAudio Class'''

from ProcessData import ProcessData

class ProcessAudio(ProcessData):

    """This class will process the audio input data before its sended to the
      neural network. It inherits from ProcessData
    """

    def process_file(self, file_name):
        """Process the data from a audio

        Args:
        file_name (str): path to the file

        Returns:
            None
        """
        pass
