'''This file defines the RNMNAppGui Class'''

import customtkinter
from RNMNApp import RNMNApp
from .RNMNGuiWindows import CustomWindow
from .RNMNGuiFrames import MainPage, SelectDataPage, CreateModelPage, PredictPage
from .RNMNGuiFrames import HiperparametersPage, MenuSelectPage, ResultsPage, TrainingPage


class RNMNAppGui(customtkinter.CTk):
    '''This class start creates the GUI for the app'''

    logic_app: RNMNApp
    frames: dict

    models: dict

    train_queue: list
    compile_queue: list

    def __init__(self, logic_app, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rely = dict()

        self.frames = dict()
        self.logic_app = logic_app
        self.resizable(width=False, height=False)

        self.models = {"text": False, "image": False, "audio": False, }
        self.train_queue = list()
        self.compile_queue = list()
        customtkinter.set_appearance_mode("dark")

        container = customtkinter.CTkFrame(self)

        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.last_frame = ""
        self.geometry(CustomWindow.center_window(
            self, 1080, 720, self._get_window_scaling()))
        self.grid_columnconfigure((0), weight=1)
        self.title("Red Neuronal Multimodal Numérica")

        for F in (MainPage, SelectDataPage, CreateModelPage,
                  HiperparametersPage, MenuSelectPage, ResultsPage, TrainingPage, PredictPage):
            page_name = F.__name__
            frame = F(logic_app=logic_app, parent=container, controller=self)
            self.frames[page_name] = frame

        self.show_frame('MainPage')

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        if self.last_frame != "":
            self.frames[self.last_frame].grid_forget()
            self.frames[self.last_frame].clean()

        self.frames[page_name].update_custom()
        aframe = self.frames[page_name]
        aframe.grid(row=0, column=0, sticky="nsew")
        self.last_frame = page_name
