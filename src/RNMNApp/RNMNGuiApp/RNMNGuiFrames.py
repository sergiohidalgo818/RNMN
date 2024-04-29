'''This file defines the RNMNAppGui Class'''

import tkinter
import customtkinter
from RNMNApp import RNMNApp
from .RNMNGuiWindows import AcceptWindow, ErrorWindow
from ..InputType import ImportError, InputType


class CustomFrame(customtkinter.CTkFrame):
    logic_app: RNMNApp
    parent: customtkinter.CTkFrame
    controller: customtkinter.CTk

    _title_font = ("Times", 35, 'bold')
    _button_font = ("Times", 25, )

    def __init__(self, logic_app, parent, controller):
        super().__init__(parent)
        self.logic_app = logic_app
        self.controller = controller


class MainPage(CustomFrame):

    def __init__(self, logic_app, parent, controller):
        super().__init__(logic_app, parent, controller)

        title = customtkinter.CTkLabel(
            self, text="Selecciona una opción", font=self._title_font)
        title.place(relx=0.5, rely=0.3, anchor=customtkinter.CENTER)

        button_load = customtkinter.CTkButton(
            self, text="Cargar modelo", command=self._load_model, font=self._button_font, width=150,
            height=50, corner_radius=20, fg_color="RoyalBlue3", hover_color="RoyalBlue4")
        button_load.place(relx=0.45, rely=0.5, anchor=customtkinter.E)

        button_create = customtkinter.CTkButton(
            self, text="Crear modelo", command=self._create_model, font=self._button_font, width=150,
            height=50, corner_radius=20, fg_color="RoyalBlue3", hover_color="RoyalBlue4")
        button_create.place(relx=0.55, rely=0.5, anchor=customtkinter.W)

    def _create_model(self):
        self.controller.show_frame("SelectDataPage")

    def _load_model(self):
        directory = customtkinter.filedialog.askopenfilename(initialdir="./",
                                                             title="Select a File",
                                                             filetypes=(("Pickle files",
                                                                         "*.pkl*"),
                                                                        ("all files",
                                                                         "*.*")))

        if len(directory) > 0:
            try:
                self.logic_app.load_model(directory)
            except ImportError as ex:
                ErrorWindow(master=self.master, controller=self.controller,
                            message="Porfavor introduzca un modelo serializado en .pkl")
            else:
                self.controller.show_frame("SelectDataPage")


class SelectDataPage(CustomFrame):


    def __init__(self, logic_app, parent, controller):

        super().__init__(logic_app, parent, controller)

        title = customtkinter.CTkLabel(
            self, text="Seleccione datos a subir", font=self._title_font)
        title.place(relx=0.5, rely=0.2, anchor=customtkinter.CENTER)

        button_text = customtkinter.CTkButton(
            self, text="Cargar datos de texto", command=self._load_text_data, font=self._button_font, width=150,
            height=50, corner_radius=20, fg_color="RoyalBlue3", hover_color="RoyalBlue4")
        button_text.place(relx=0.5, rely=0.35, anchor=customtkinter.CENTER)

        button_audio = customtkinter.CTkButton(
            self, text="Cargar datos de audio", command=self._load_audio_data, font=self._button_font, width=150,
            height=50, corner_radius=20, fg_color="RoyalBlue3", hover_color="RoyalBlue4")
        button_audio.place(relx=0.5, rely=0.48, anchor=customtkinter.CENTER)

        button_image = customtkinter.CTkButton(
            self, text="Cargar datos de imagen", command=self._load_image_data, font=self._button_font, width=150,
            height=50, corner_radius=20, fg_color="RoyalBlue3", hover_color="RoyalBlue4")
        button_image.place(relx=0.5, rely=0.61, anchor=customtkinter.CENTER)

        button_cancel = customtkinter.CTkButton(
            self, text="Cancelar", command=self._cancel, font=self._button_font, width=150,
            height=50, corner_radius=20, fg_color="brown3", hover_color="brown4")
        button_cancel.place(relx=0.45, rely=0.8, anchor=customtkinter.E)

        button_accept = customtkinter.CTkButton(
            self, text="Aceptar", command=self._accept, font=self._button_font, width=150,
            height=50, corner_radius=20, fg_color="lime green", hover_color="forest green")
        button_accept.place(relx=0.55, rely=0.8, anchor=customtkinter.W)

    def _load_text_data(self):

        directory = customtkinter.filedialog.askdirectory(initialdir="./",
                                                          title="Seleccione un directorio de datos de texto")
        if len(directory) > 0:
            try:
                self.logic_app.get_text_data(directory)
            except ImportError as ex:
                ErrorWindow(self.master, self.controller,
                            message="Porfavor, introduzca un directorio con archivos.parquet")
            else:
                try:
                    self.logic_app.preprocess_typedata_data([InputType.TEXT])
                except ImportError:
                    ErrorWindow(self.master, self.controller,
                                message="Error al importar archivos, compruebe su extension y directorio")

    def _load_audio_data(self):
        directory = customtkinter.filedialog.askdirectory(initialdir="./",
                                                          title="Seleccione un directorio de datos de audio")

        if len(directory) > 0:
            try:
                self.logic_app.get_audio_data(directory)
            except ImportError as ex:
                ErrorWindow(self.master, self.controller,
                            message="Porfavor, introduzca un directorio con archivos de audio")
            else:
                try:
                    self.logic_app.preprocess_typedata_data([InputType.AUDIO])
                except ImportError:
                    ErrorWindow(self.master, self.controller,
                                message="Error al importar archivos, compruebe su extension y directorio")

    def _load_image_data(self):
        directory = customtkinter.filedialog.askdirectory(initialdir="./",
                                                          title="Seleccione un directorio de datos de imagen")

        if len(directory) > 0:
            try:
                self.logic_app.get_image_data(directory)
            except ImportError as ex:
                ErrorWindow(self.master, self.controller,
                            message="Porfavor, introduzca un directorio con archivos de imagen")
            else:
                try:
                    self.logic_app.preprocess_typedata_data([InputType.IMAGE])
                except ImportError:
                    ErrorWindow(self.master, self.controller,
                                message="Error al importar archivos, compruebe su extension y directorio")

    def _cancel(self):
        AcceptWindow(master=self.master, controller=self.controller,
                     message="¿Seguro que desea cancelar la carga de datos?")
        boolvar = customtkinter.BooleanVar(self.master, name="window_accept")

        if boolvar.get():
            self.controller.show_frame("MainPage")

    def _accept(self):
        AcceptWindow(master=self.master, controller=self.controller,
                     message="¿Seguro que desea iniciar creación con estos datos?")
        boolvar = customtkinter.BooleanVar(self.master, name="window_accept")

        if boolvar.get():
            try:
                self.logic_app.create_model() # here detects if there is data loaded
            except ImportError:
                ErrorWindow(self.master, self.controller,
                            message="Error al importar archivos, compruebe su extension y directorio")
            else:
                self.controller.show_frame("HiperparametersPage")


class HiperparametersPage(CustomFrame):


    def __init__(self, logic_app, parent, controller):
        super().__init__(logic_app, parent, controller)

        self.logic_app = logic_app
        self.controller = controller

        title = customtkinter.CTkLabel(
            self, text="Introducir hiperparámetros", font=self._title_font)
        title.pack(padx=10, pady=50)
