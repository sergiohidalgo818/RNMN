'''This file defines the RNMNApp Class'''

import tkinter
import customtkinter

from .RNMNAppGui import RNMNAppGui

class RNMNApp():
    """This class start the app and get the location of the data and
      the trained model (if it exists) 
    """
    data_and_types : dict
    
    app_gui : RNMNAppGui

    def __init__(self) -> None:
        pass
    
    def start_app(self):
        pass

    def get_text_data(directory:str):
        pass

    def get_audio_data(directory:str):
        pass
    
    def get_image_data(directory:str):
        pass
    


    def _app_gui(self):
        self.app_gui = RNMNAppGui(self)

        self.app_gui.mainloop()
