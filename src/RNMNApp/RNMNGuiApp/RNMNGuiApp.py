'''This file defines the RNMNAppGui Class'''

import tkinter
import customtkinter
from RNMNApp import RNMNApp
from ..InputType import ImportError, InputType
from .RNMNGuiWindows import AcceptWindow, ErrorWindow, CustomWindow
from .RNMNGuiFrames import CustomFrame, MainPage, HiperparametersPage, SelectDataPage

class RNMNAppGui(customtkinter.CTk):
    '''This class start creates the GUI for the app'''

    logic_app: RNMNApp
    frames: dict

    def __init__(self, logic_app, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.frames = dict()
        self.logic_app = logic_app

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

        for F in (MainPage, SelectDataPage, HiperparametersPage):
            page_name = F.__name__
            frame = F(logic_app=logic_app, parent=container, controller=self)
            self.frames[page_name] = frame

        self.show_frame('MainPage')

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        if self.last_frame != "":
            self.frames[self.last_frame].grid_forget()
        aframe = self.frames[page_name]
        aframe.grid(row=0, column=0, sticky="nsew")
        self.last_frame = page_name