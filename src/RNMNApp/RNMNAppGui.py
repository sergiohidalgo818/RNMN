'''This file defines the RNMNAppGui Class'''

import tkinter
import customtkinter
from RNMNApp import RNMNApp
from .InputType import ImportError
from ProcessData import ProcessError

class ErrorWindow(customtkinter.CTkToplevel):
    def __init__(self,  master, controller:customtkinter.CTk, message, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.master=master
        self.controller=controller

        self.geometry("520x460")

        self.label = customtkinter.CTkLabel(self, text=message)
        self.label.pack(padx=20, pady=20)

        button = customtkinter.CTkButton(
            self, text="Aceptar", command=self.accept, width=100, height=100)
        button.pack(padx=10, pady=50)

        self.wait_visibility()
        self.transient(master) # set to be on top of the main window
        self.grab_set() # hijack all commands from the master (clicks on the main window are ignored)
        master.wait_window(self) # pause anything on the main window until this one closes


    def accept(self):
        self.destroy()


class AcceptWindow(customtkinter.CTkToplevel):
    def __init__(self,  master, controller:customtkinter.CTk, message, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.master=master
        self.controller=controller

        self.geometry("520x460")

        self.label = customtkinter.CTkLabel(self, text=message)
        self.label.pack(padx=20, pady=20)
        button = customtkinter.CTkButton(
            self, text="Cancelar", command=self.cancel, width=100, height=100)
        button.pack(padx=10, pady=50)
        
        button2 = customtkinter.CTkButton(
            self, text="Aceptar", command=self.accept, width=100, height=100)
        button2.pack(padx=10, pady=50)

        self.wait_visibility()
        self.transient(master) # set to be on top of the main window
        self.grab_set() # hijack all commands from the master (clicks on the main window are ignored)
        master.wait_window(self) # pause anything on the main window until this one closes

    def cancel(self):
        self.master.setvar(name="window_accept", value = False)
        self.destroy()

    def accept(self):
        self.master.setvar(name="window_accept", value = True)
        self.destroy()


class RNMNAppGui(customtkinter.CTk):
    '''This class start creates the GUI for the app'''

    logic_app: RNMNApp
    frames: dict


    _title_font = ("Times", 40, )
    _button_font = ("Times", 30, 'bold')
    _accept_window = False

    def __init__(self, logic_app, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.frames = dict()
        self.logic_app = logic_app

    
        customtkinter.set_appearance_mode("dark")
        customtkinter.set_default_color_theme("blue")

        container = customtkinter.CTkFrame(self)

        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.last_frame = ""
        self.geometry("1080x720")
        self.grid_columnconfigure((0), weight=1)
        self.title("Red Neuronal Multimodal Numérica")

        for F in (MainPage, SelectDataPage, InfoPage):
            page_name = F.__name__
            frame = F(logic_app=logic_app, parent=container, controller=self)
            self.frames[page_name] = frame
        

        self._error_window = None

        self.show_frame('MainPage')
        


    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        if self.last_frame != "":
            self.frames[self.last_frame].grid_forget()
        aframe = self.frames[page_name]
        aframe.grid(row=0, column=0, sticky="nsew")
        self.last_frame = page_name
    
    def open_error_window(self):
        if self._error_window is None or not self._error_window.winfo_exists():
            self._error_window = ErrorWindow(self)  # create window if its None or destroyed
        else:
            self._error_window.focus()
        

class MainPage(customtkinter.CTkFrame):


    logic_app: RNMNApp
    parent: customtkinter.CTkFrame
    controller: customtkinter.CTk

    _title_font = ("Times", 40, )
    _button_font = ("Times", 30, 'bold')

    def __init__(self, logic_app, parent, controller):
        super().__init__(parent)
        
        self.logic_app = logic_app
        self.controller = controller

        title = customtkinter.CTkLabel(
            self, text="Selecciona una opción", font=self._title_font)
        title.pack(padx=10, pady=50)
        button = customtkinter.CTkButton(
            self, text="Cargar modelo", command=self._load_model, font=self._button_font, width=200, height=100)
        button.pack(padx=10, pady=50)
        button2 = customtkinter.CTkButton(
            self, text="Crear modelo", command=self._create_model, font=self._button_font, width=200, height=100)
        button2.pack(padx=10, pady=50)

    def _create_model(self):
        self.controller.show_frame("SelectDataPage")
        

    def _load_model(self):
        directory = customtkinter.filedialog.askopenfilename(initialdir="./",
                                                             title="Select a File",
                                                             filetypes=(("Pickle files",
                                                                         "*.pkl*"),
                                                                        ("all files",
                                                                         "*.*")))

        try:
            self.logic_app.load_model(directory)
        except (FileNotFoundError, TypeError):
            pass # to prevent file errors when window is closed
        except ImportError as ex:
            ErrorWindow(self.master, self.controller, message="Porfavor introduzca un modelo serializado en .pkl")
        else:
            self.controller.show_frame("SelectDataPage")

        

class SelectDataPage(customtkinter.CTkFrame):

    logic_app: RNMNApp
    parent: customtkinter.CTkFrame
    controller: RNMNAppGui

    _title_font = ("Times", 40, )
    _button_font = ("Times", 30, 'bold')

    def __init__(self, logic_app, parent, controller):
        super().__init__(parent)

        self.logic_app = logic_app
        self.controller = controller

        title = customtkinter.CTkLabel(
            self, text="Selecciona datos a subir", font=self._title_font)
        title.pack(padx=10, pady=20)
        button = customtkinter.CTkButton(
            self, text="Cargar datos de texto", command=self._load_text_data, font=self._button_font, width=200, height=100)
        button.pack(padx=10, pady=20)
        button2 = customtkinter.CTkButton(
            self, text="Cargar datos de audio", command=self._load_audio_data, font=self._button_font, width=200, height=100)
        button2.pack(padx=10, pady=20)
        button3 = customtkinter.CTkButton(
            self, text="Cargar datos de imagen", command=self._load_image_data, font=self._button_font, width=200, height=100)
        button3.pack(padx=10, pady=20)

        button4 = customtkinter.CTkButton(
            self, text="Cancelar", command=self._cancel, font=self._button_font, width=100, height=100)
        button4.pack(padx=10, pady=20)

        button5 = customtkinter.CTkButton(
            self, text="Procesar", command=self._process, font=self._button_font, width=100, height=100)
        button5.pack(padx=10, pady=20)



    def _load_text_data(self):
        directory = customtkinter.filedialog.askdirectory(initialdir="./",
                                               title="Selecciona un directorio de datos de texto")
        
        try:
            self.logic_app.get_text_data(directory)
        except (FileNotFoundError, TypeError):
            pass # to prevent file errors when window is closed
        except ImportError as ex:
            ErrorWindow(self.master, self.controller, message="Porfavor, introduzca un directorio con archivos.parquet")
            
    def _load_audio_data(self):
        directory = customtkinter.filedialog.askdirectory(initialdir="./",
                                               title="Selecciona un directorio de datos de audio")
        
        try:
            self.logic_app.get_audio_data(directory)
        except (FileNotFoundError, TypeError):
            pass # to prevent file errors when window is closed
        except ImportError as ex:
            ErrorWindow(self.master, self.controller, message="Porfavor, introduzca un directorio con archivos de audio")
        
    def _load_image_data(self):
        directory = customtkinter.filedialog.askdirectory(initialdir="./",
                                               title="Selecciona un directorio de datos de imagen")
        
        try:
            self.logic_app.get_image_data(directory)
        except (FileNotFoundError, TypeError):
            pass # to prevent file errors when window is closed
        except ImportError as ex:
            ErrorWindow(self.master, self.controller, message="Porfavor, introduzca un directorio con archivos de imagen")

    def _cancel(self):
        AcceptWindow(self.master, self.controller, message="¿Seguro que desea cancelar la carga de datos?")
        boolvar = customtkinter.BooleanVar(self.master, name="window_accept")
        
        if boolvar.get():
            self.controller.show_frame("MainPage")


    def _process(self):
        AcceptWindow(self.master, self.controller, message="¿Seguro que desea procesar los datos?")
        boolvar = customtkinter.BooleanVar(self.master, name="window_accept", message="¿Seguro que desea procesar los datos?")
        
        if boolvar.get():
            self.logic_app.preprocess_data()
            self.controller.show_frame("InfoPage")




class InfoPage(customtkinter.CTkFrame):


    logic_app: RNMNApp
    parent: customtkinter.CTkFrame
    controller: customtkinter.CTk

    _title_font = ("Times", 40, )
    _button_font = ("Times", 30, 'bold')

    def __init__(self, logic_app, parent, controller):
        super().__init__(parent)
        
        self.logic_app = logic_app
        self.controller = controller

        title = customtkinter.CTkLabel(
            self, text="Informacion aqui", font=self._title_font)
        title.pack(padx=10, pady=50)
