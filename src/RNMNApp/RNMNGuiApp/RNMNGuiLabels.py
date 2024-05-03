'''This file defines the RNMNAppGui Class'''

import tkinter
import tkinter.font
import customtkinter
from RNMNParent import RNMNParams
import json


class CustomLabel(customtkinter.CTkLabel):
    _title_font = ("Times", 25, 'bold')
    _button_font = ("Times", 20, )

    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs, width=1080, height=720, text="", bg_color="gray17")

