'''This file defines the RNMNAppGui Class'''

import tkinter
import customtkinter
from RNMNApp import RNMNApp

class _LoadModelWindow(customtkinter.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("400x300")

        self.label = customtkinter.CTkLabel(self, text="Browse Model")
        self.label.pack(padx=20, pady=20)


class RNMNAppGui(customtkinter.CTk):
    '''This class start creates the GUI for the app'''

    logic_app : RNMNApp
    
    _title_font  = ("Times",40, )
    _button_font  = ("Times",30,'bold')
    _load_model_window : _LoadModelWindow
    

    def __init__(self, logic_app, *args, **kwargs):
            super().__init__(*args, **kwargs)

            self.logic_app = logic_app
            customtkinter.set_appearance_mode("dark")
            customtkinter.set_default_color_theme("dark-blue")

            self.toplevel_window = None
            self.geometry("1080x720")
            self.grid_columnconfigure((0), weight=1)
            self.title("Red Neuronal Multimodal Numérica")
            title = customtkinter.CTkLabel(self, text="Selecciona una opción", font=self._title_font)
            title.pack(padx=10, pady=50)
            button = customtkinter.CTkButton(self, text="Cargar modelo", command=self._load_model, font=self._button_font, width=200, height=100)
            button.pack(padx=10, pady=50)
            button2 = customtkinter.CTkButton(self, text="Crear modelo", command=self._create_model, font=self._button_font, width=200, height=100)
            button2.pack(padx=10, pady=50)
            self._load_model_window = None
    

    def _create_model(self):
        pass

    def _load_model(self):
        if self._load_model_window is None or not self._load_model_window.winfo_exists():
            self._load_model_window = _LoadModelWindow(self)  # create window if its None or destroyed
        else:
            self._load_model_window.focus()  # if window exists focus it



        


