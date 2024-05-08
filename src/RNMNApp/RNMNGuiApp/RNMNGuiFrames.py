'''This file defines the RNMNAppGuiFrames Class'''

import customtkinter
from RNMNApp import RNMNApp
from .RNMNGuiWindows import AcceptWindow, ErrorWindow, PredictWindow, GraphWindow
from ..InputType import ImportError, InputType
from .RNMNGuiTabs import CreateNetTabView, ValidationTabError
from .RNMNGuiLabels import CustomLabel
from RNMNParent import RNMNParams
import threading
import time
import os
import numpy as np
from PIL import Image, ImageDraw
import pandas as pd

import tensorflow


class CustomFrame(customtkinter.CTkFrame):
    """Custom frame class
    """
    logic_app: RNMNApp
    parent: customtkinter.CTkFrame
    controller: customtkinter.CTk

    _title_font = ("Times", 35, 'bold')
    _button_font = ("Times", 25, )

    def __init__(self, logic_app, parent, controller):
        super().__init__(parent)
        self.logic_app = logic_app
        self.controller = controller

    def clean(self):
        pass

    def update_custom(self):
        pass


class MainPage(CustomFrame):
    """This is the main page of the GUI
    """

    def __init__(self, logic_app, parent, controller):
        super().__init__(logic_app, parent, controller)

        title = customtkinter.CTkLabel(
            self, text="Seleccione una opción", font=self._title_font)
        title.place(relx=0.5, rely=0.3, anchor=customtkinter.CENTER)

        button_load = customtkinter.CTkButton(
            self, text="Cargar modelo", command=self._load_model, font=self._button_font, width=150,
            height=50, corner_radius=20, fg_color="RoyalBlue3", hover_color="RoyalBlue4")
        button_load.place(relx=0.45, rely=0.5, anchor=customtkinter.E)

        button_create = customtkinter.CTkButton(
            self, text="Crear modelo", command=self._create_model, font=self._button_font, width=150,
            height=50, corner_radius=20, fg_color="RoyalBlue3", hover_color="RoyalBlue4")
        button_create.place(relx=0.55, rely=0.5, anchor=customtkinter.W)

        self.button_load = customtkinter.CTkButton(
            self, text="Cargar configuración", command=self._load, font=self._button_font, width=150,
            height=50, corner_radius=20, fg_color="RoyalBlue3", hover_color="RoyalBlue4")
        self.button_load.place(relx=0.5, rely=0.65,
                               anchor=customtkinter.CENTER)

    def _create_model(self):
        if self.logic_app._has_model:
            del self.logic_app.model
        self.controller.show_frame("CreateModelPage")

    def _load(self):
        file_config = customtkinter.filedialog.askopenfile(initialdir=self.logic_app.config_path,
                                                           title="Seleciona un archivo de configuración",
                                                           filetypes=(("JSON files",
                                                                       "*.json*"),
                                                                      ("all files",
                                                                       "*.*")))
        if file_config != None:
            try:
                params_dict = self.logic_app.json_transform(file_config.read())
            except ImportError as ex:
                ErrorWindow(self.master, self.controller,
                            message="Porfavor, introduzca un fichero json")
            else:
                if "text_config" in params_dict.keys():
                    self.controller.models['text'] = True
                if "audio_config" in params_dict.keys():
                    self.controller.models['audio'] = True
                if "image_config" in params_dict.keys():
                    self.controller.models['image'] = True

                self.logic_app.model_params = params_dict
                self.controller.show_frame("SelectDataPage")

    def _load_model(self):
        directory = customtkinter.filedialog.askopenfilename(initialdir="./",
                                                             title="Selecciona un modelo ya guardado",
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
                self.controller.show_frame("MenuSelectPage")


class SelectDataPage(CustomFrame):
    """Here is where the data for training
        the model is selected
    """

    _button_text: customtkinter.CTkButton
    _button_audio: customtkinter.CTkButton
    _button_image: customtkinter.CTkButton

    _button_text_recover: customtkinter.CTkButton
    _button_audio_recover: customtkinter.CTkButton
    _button_image_recover: customtkinter.CTkButton

    _text_data: customtkinter.CTkLabel
    _audio_data: customtkinter.CTkLabel
    _image_data: customtkinter.CTkLabel

    _data_counter: int

    _data_to_clear: set

    def __init__(self, logic_app, parent, controller):

        super().__init__(logic_app, parent, controller)

        self._data_counter = 0
        self._data_to_clear = set()
        self.rely = dict()

        title = customtkinter.CTkLabel(
            self, text="Seleccione datos a subir", font=self._title_font)
        title.place(relx=0.5, rely=0.1, anchor=customtkinter.CENTER)

        self.label = CustomLabel(master=self)
        self.label.place(relx=0.5, rely=0.7, anchor=customtkinter.CENTER)

        self.rely = {"text": 0, "audio": 0, "image": 0}

        button_cancel = customtkinter.CTkButton(
            self, text="Cancelar", command=self._cancel, font=self._button_font, width=150,
            height=50, corner_radius=20, fg_color="brown3", hover_color="brown4", bg_color="gray17")
        button_cancel.place(relx=0.2, rely=0.9, anchor=customtkinter.E)

        button_accept = customtkinter.CTkButton(
            self, text="Aceptar", command=self._accept, font=self._button_font, width=150,
            height=50, corner_radius=20, fg_color="lime green", hover_color="forest green", bg_color="gray17")
        button_accept.place(relx=0.8, rely=0.9, anchor=customtkinter.W)

    def add_text_button(self):
        self._text_data = customtkinter.CTkLabel(
            self.label, text="Datos de texto añadidos correctamente", font=self._button_font)
        self._button_text_recover = customtkinter.CTkButton(self.label, text="Eliminar datos de texto",
                                                            command=self._recover_text_button, font=self._button_font, width=150,
                                                            height=50, corner_radius=20, fg_color="brown3", hover_color="brown4", bg_color="gray17")

        self._button_text = customtkinter.CTkButton(
            self.label, text="Cargar datos de texto", command=self._load_text_data, font=self._button_font, width=150,
            height=50, corner_radius=20, fg_color="RoyalBlue3", hover_color="RoyalBlue4", bg_color="gray17")
        self._button_text.place(relx=0.5, rely=self.rely['text'],
                                anchor=customtkinter.CENTER)

    def add_audio_button(self):
        self._audio_data = customtkinter.CTkLabel(
            self.label, text="Datos de audio añadidos correctamente", font=self._button_font)
        self._button_audio_recover = customtkinter.CTkButton(self.label, text="Eliminar datos de audio",
                                                             command=self._recover_audio_button, font=self._button_font, width=150,
                                                             height=50, corner_radius=20, fg_color="brown3", hover_color="brown4", bg_color="gray17")

        self._button_audio = customtkinter.CTkButton(
            self.label, text="Cargar datos de audio", command=self._load_audio_data, font=self._button_font, width=150,
            height=50, corner_radius=20, fg_color="RoyalBlue3", hover_color="RoyalBlue4", bg_color="gray17")
        self._button_audio.place(
            relx=0.5, rely=self.rely['audio'], anchor=customtkinter.CENTER)

    def add_image_button(self):
        self._image_data = customtkinter.CTkLabel(
            self.label, text="Datos de imagen añadidos correctamente", font=self._button_font)
        self._button_image_recover = customtkinter.CTkButton(self.label, text="Eliminar datos de imagen",
                                                             command=self._recover_image_button, font=self._button_font, width=150,
                                                             height=50, corner_radius=20, fg_color="brown3", hover_color="brown4", bg_color="gray17")
        self._button_image = customtkinter.CTkButton(
            self.label, text="Cargar datos de imagen", command=self._load_image_data, font=self._button_font, width=150,
            height=50, corner_radius=20, fg_color="RoyalBlue3", hover_color="RoyalBlue4", bg_color="gray17")
        self._button_image.place(
            relx=0.5, rely=self.rely['image'], anchor=customtkinter.CENTER)

    def _recover_text_button(self):
        self._text_data.place_forget()
        self._button_text_recover.place_forget()
        self._button_text.place(relx=0.5, rely=self.rely['text'],
                                anchor=customtkinter.CENTER)
        self._data_counter -= 1
        self._data_to_clear.remove(self._recover_text_button)

    def _recover_audio_button(self):
        self._audio_data.place_forget()
        self._button_audio_recover.place_forget()
        self._button_audio.place(relx=0.5, rely=self.rely['audio'],
                                 anchor=customtkinter.CENTER)
        self._data_counter -= 1
        self._data_to_clear.remove(self._recover_audio_button)

    def _recover_image_button(self):
        self._image_data.place_forget()
        self._button_image_recover.place_forget()
        self._button_image.place(
            relx=0.5, rely=self.rely['image'], anchor=customtkinter.CENTER)
        self._data_counter -= 1
        self._data_to_clear.remove(self._recover_image_button)

    def _load_text_data(self):

        directory = customtkinter.filedialog.askdirectory(initialdir=os.path.join(self.logic_app.workdir, "data"),
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
                else:
                    self._button_text.place_forget()
                    self._text_data.place(
                        relx=0.5, rely=self.rely['text'], anchor=customtkinter.E)
                    self._button_text_recover.place(
                        relx=0.55, rely=self.rely['text'], anchor=customtkinter.W)
                    self._data_counter += 1
                    self._data_to_clear.add(self._recover_text_button)

    def _load_audio_data(self):
        directory = customtkinter.filedialog.askdirectory(initialdir=os.path.join(self.logic_app.workdir, "data"),
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
                else:
                    self._button_audio.place_forget()
                    self._audio_data.place(
                        relx=0.5, rely=self.rely['audio'], anchor=customtkinter.E)
                    self._button_audio_recover.place(
                        relx=0.55, rely=self.rely['audio'], anchor=customtkinter.W)
                    self._data_counter += 1
                    self._data_to_clear.add(self._recover_audio_button)

    def _load_image_data(self):
        directory = customtkinter.filedialog.askdirectory(initialdir=os.path.join(self.logic_app.workdir, "data"),
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
                else:
                    self._button_image.place_forget()
                    self._image_data.place(
                        relx=0.5, rely=self.rely['image'], anchor=customtkinter.E)
                    self._button_image_recover.place(
                        relx=0.55, rely=self.rely['image'], anchor=customtkinter.W)
                    self._data_counter += 1
                    self._data_to_clear.add(self._recover_image_button)

    def _cancel(self):
        AcceptWindow(master=self.master, controller=self.controller,
                     message="¿Seguro que desea cancelar la carga de datos?")
        boolvar = customtkinter.BooleanVar(self.master, name="window_accept")
        if boolvar.get():
            if self._data_counter != self.model_cont:
                for fun in self._data_to_clear.copy():
                    fun()

                self.controller.show_frame("MainPage")

    def _accept(self):

        if self._data_counter != self.model_cont:
            if self.model_cont == 1:
                ErrorWindow(master=self.master, controller=self.controller,
                            message="Añada los datos para el entrenamiento para el modelo, porfavor")
            else:
                ErrorWindow(master=self.master, controller=self.controller,
                            message="Añada los datos para el entrenamiento para todos los modelos, porfavor")

        else:
            AcceptWindow(master=self.master, controller=self.controller,
                         message="¿Seguro que desea proceder con estos datos?")
            boolvar = customtkinter.BooleanVar(
                self.master, name="window_accept")

            if boolvar.get():
                self.logic_app.create_model()
                self.controller.show_frame("HiperparametersPage")

    def update_custom(self):

        self.rely['text'] = 0
        self.rely['audio'] = 0
        self.rely['image'] = 0

        rel = 0

        self.model_cont = 0

        for key in self.controller.models:
            if self.controller.models[key]:
                self.model_cont += 1

        if self.model_cont == 1:
            rel = 0.3

        if self.model_cont == 2:
            rel = 0.19

        if self.model_cont == 3:
            rel = 0.15

        rel_sum = 0

        if self.controller.models['text']:
            rel_sum += rel
            self.rely['text'] = rel_sum
            self.controller.rely['text'] = rel_sum
            self.add_text_button()

        if self.controller.models['audio']:
            rel_sum += rel
            self.rely['audio'] = rel_sum
            self.controller.rely['audio'] = rel_sum
            self.add_audio_button()

        if self.controller.models['image']:
            rel_sum += rel
            self.rely['image'] = rel_sum
            self.controller.rely['image'] = rel_sum
            self.add_image_button()

    def clean(self):

        if self.controller.models['text']:
            if InputType.TEXT in self.logic_app.preprocessed_data_and_types.keys():
                self._recover_text_button()
                self._button_text.place_forget()
            else:
                self._button_text.place_forget()

        if self.controller.models['audio']:
            if InputType.AUDIO in self.logic_app.preprocessed_data_and_types.keys():
                self._recover_audio_button()
                self._button_audio.place_forget()
            else:
                self._button_audio.place_forget()

        if self.controller.models['image']:
            if InputType.IMAGE in self.logic_app.preprocessed_data_and_types.keys():
                self._recover_image_button()
                self._button_image.place_forget()
            else:
                self._button_image.place_forget()


class CreateModelPage(CustomFrame):
    """Here the architecture and models of the big model are selected
    """

    def __init__(self, logic_app, parent, controller):
        super().__init__(logic_app, parent, controller)
        self.logic_app = logic_app
        self.controller = controller

        title = customtkinter.CTkLabel(
            master=self, text="Creación de la red", font=self._title_font)
        title.place(relx=0.5, rely=0.1, anchor=customtkinter.CENTER)

        self.tab_view = CreateNetTabView(master=self, width=1080, height=720)
        self.tab_view.place(relx=0.5, rely=0.7, anchor=customtkinter.CENTER)

        self.button_cancel = customtkinter.CTkButton(
            self, text="Cancelar", command=self._cancel, font=self._button_font, width=150,
            height=50, corner_radius=20, fg_color="brown3", hover_color="brown4")
        self.button_cancel.place(relx=0.2, rely=0.9, anchor=customtkinter.E)

        self.button_create = customtkinter.CTkButton(
            self, text="Crear", command=self._create, font=self._button_font, width=150,
            height=50, corner_radius=20, fg_color="lime green", hover_color="forest green")
        self.button_create.place(relx=0.8, rely=0.9, anchor=customtkinter.W)

    def _get_params(self, model_name: InputType) -> dict:
        try:
            self.tab_view.validate()
        except ValidationTabError:
            raise ValidationTabError("Error on input parameters")
        else:
            params_dict = dict()
            params_dict['num_inputs'] = self.tab_view.params_dict[model_name]['num_inputs'].get()
            params_dict['layers_dict'] = dict()

            for layer in self.tab_view.params_dict[model_name]['layers_dict']:
                params_dict['layers_dict'][layer] = dict()
                for key in self.tab_view.params_dict[model_name]['layers_dict'][layer]:
                    params_dict['layers_dict'][layer][key] = self.tab_view.params_dict[model_name]['layers_dict'][layer][key].get(
                    )

            return params_dict

    def _create(self):

        params_dict = {}

        var_text = customtkinter.BooleanVar(
            master=self.master, name="switch_texto")

        var_audio = customtkinter.BooleanVar(
            master=self.master, name="switch_audio")

        var_image = customtkinter.BooleanVar(
            master=self.master, name="switch_imagen")

        number_of_models = 0

        self.controller.models['text'] = self.tab_view.params_dict['texto']['add_model'].get(
        )
        self.controller.models['audio'] = self.tab_view.params_dict['audio']['add_model'].get(
        )
        self.controller.models['image'] = self.tab_view.params_dict['imagen']['add_model'].get(
        )

        try:
            if var_text.get():
                number_of_models += 1
                params_dict['text_config'] = self._get_params("texto")

            if var_audio.get():
                number_of_models += 1
                params_dict['audio_config'] = self._get_params("audio")

            if var_image.get():
                number_of_models += 1
                params_dict['image_config'] = self._get_params("imagen")

        except ValidationTabError:
            ErrorWindow(master=self.master, controller=self.controller,
                        message="Porfavor introduzca un valor numérico superior\na 0 en el número de entradas y salidas")
        else:
            if number_of_models == 0:
                ErrorWindow(master=self.master, controller=self.controller,
                            message="Porfavor elija al menos un modelo")
            else:
                self.logic_app.model_params = params_dict

                self.controller.show_frame("SelectDataPage")

    def _cancel(self):
        AcceptWindow(master=self.master, controller=self.controller,
                     message="¿Seguro que desea cancelar la creación del modelo?")
        boolvar = customtkinter.BooleanVar(self.master, name="window_accept")
        if boolvar.get():
            self.controller.show_frame("MainPage")

    def clean(self):
        self.tab_view.destroy()
        self.tab_view = CreateNetTabView(master=self, width=1080, height=720)
        self.tab_view.place(relx=0.5, rely=0.7, anchor=customtkinter.CENTER)

        self.button_cancel = customtkinter.CTkButton(
            self, text="Cancelar", command=self._cancel, font=self._button_font, width=150,
            height=50, corner_radius=20, fg_color="brown3", hover_color="brown4")
        self.button_cancel.place(relx=0.2, rely=0.9, anchor=customtkinter.E)

        self.button_create = customtkinter.CTkButton(
            self, text="Crear", command=self._create, font=self._button_font, width=150,
            height=50, corner_radius=20, fg_color="lime green", hover_color="forest green")
        self.button_create.place(relx=0.8, rely=0.9, anchor=customtkinter.W)


class HiperparametersPage(CustomFrame):
    """This view is for the compile parameters 
    """

    def __init__(self, logic_app, parent, controller):
        super().__init__(logic_app, parent, controller)

        self.logic_app = logic_app
        self.controller = controller

        title = customtkinter.CTkLabel(
            self, text="Configruración de parámetros", font=self._title_font)
        title.place(relx=0.5, rely=0.1, anchor=customtkinter.CENTER)

        self.label = CustomLabel(master=self)
        self.label.place(relx=0.5, rely=0.7, anchor=customtkinter.CENTER)

        self.losses = [loss.value for loss in RNMNParams.RNMNLosses]
        self.optimizers = [
            optimizer.value for optimizer in RNMNParams.RNMNOptimizers]
        self.metrics = [metric.value for metric in RNMNParams.RNMNMetrics]

        self.model_frame_create()

        button_cancel = customtkinter.CTkButton(
            self, text="Cancelar", command=self._cancel, font=self._button_font, width=150,
            height=50, corner_radius=20, fg_color="brown3", hover_color="brown4", bg_color="gray17")
        button_cancel.place(relx=0.2, rely=0.9, anchor=customtkinter.E)

        button_create = customtkinter.CTkButton(
            self, text="Confirmar", command=self._confirm, font=self._button_font, width=150,
            height=50, corner_radius=20, fg_color="lime green", hover_color="forest green", bg_color="gray17")
        button_create.place(relx=0.8, rely=0.9, anchor=customtkinter.W)

    def model_frame_create(self):

        optimizer_var: customtkinter.StringVar
        loss_var: customtkinter.StringVar
        title: str

        title = customtkinter.CTkLabel(
            self.label, text="Ajustar losses", font=self._button_font, bg_color="gray17")
        title.place(relx=0.2, rely=0.25,
                    anchor=customtkinter.CENTER)
        loss_var = customtkinter.StringVar(
            master=self.master, value=self.losses[0], name="loss")
        combobox_loss = customtkinter.CTkComboBox(master=self.label, values=self.losses,
                                                  state="readonly",
                                                  variable=loss_var, width=153, bg_color="gray17")
        combobox_loss.place(relx=0.35, rely=0.25, anchor=customtkinter.CENTER)

        title = customtkinter.CTkLabel(
            master=self.label, text="Ajustar optimizer", font=self._button_font, bg_color="gray17")
        title.place(relx=0.2, rely=0.35, anchor=customtkinter.CENTER)
        optimizer_var = customtkinter.StringVar(
            master=self.master, value=self.optimizers[0], name="optimizer")
        combobox_optimizer = customtkinter.CTkComboBox(master=self.label, values=self.optimizers,
                                                       state="readonly",
                                                       variable=optimizer_var, width=100, bg_color="gray17")
        combobox_optimizer.place(
            relx=0.35, rely=0.35, anchor=customtkinter.CENTER)

        title = customtkinter.CTkLabel(
            master=self.label, text="Seleccionar las métricas deseadas", font=self._button_font, bg_color="gray17")
        title.place(relx=0.63, rely=0.1,
                    anchor=customtkinter.CENTER)

        cont = 1
        contx = 0.64
        conty = 0
        for metric in self.metrics:

            value = False
            if cont == 1:
                value = True

            check_var = customtkinter.BooleanVar(
                master=self.master, value=value, name=metric)

            checbox = customtkinter.CTkCheckBox(master=self.label,
                                                text=metric,
                                                variable=check_var, onvalue=True, offvalue=False, bg_color="gray17")

            checbox.place(
                relx=contx, rely=0.2+conty, anchor=customtkinter.W)

            if cont % 2 == 0:
                cont += 1
                conty += 0.1
                contx = 0.64
            else:
                cont += 1
                contx = 0.5

    def _get_params(self) -> dict:
        aux_dict = dict()

        loss = customtkinter.StringVar(
            master=self.master, name="loss")

        aux_dict['loss'] = loss.get()

        optimizer = customtkinter.StringVar(
            master=self.master, name="optimizer")

        aux_dict['optimizer'] = optimizer.get()

        metrics_names = [(metric.value) for metric in RNMNParams.RNMNMetrics]

        metrics = list()

        for metric in metrics_names:
            metric_var = customtkinter.BooleanVar(
                master=self.master, name=metric)
            if metric_var.get():
                metrics.append(metric)

        aux_dict['metrics'] = metrics

        return aux_dict

    def _confirm(self):

        params_dict = self._get_params()

        self.logic_app.compile_model(params_dict)

        self.controller.show_frame("TrainingPage")

    def _cancel(self):
        AcceptWindow(master=self.master, controller=self.controller,
                     message="¿Seguro que desea cancelar la configuración del modelo?")
        boolvar = customtkinter.BooleanVar(self.master, name="window_accept")
        if boolvar.get():
            if self.logic_app._has_model:
                self.controller.show_frame("MenuSelectPage")
            else:
                self.controller.show_frame("MainPage")


class MenuSelectPage(CustomFrame):
    """The page with the model already trained ready to predict
    """

    def __init__(self, logic_app, parent, controller):
        super().__init__(logic_app, parent, controller)

        self.logic_app = logic_app
        self.controller = controller

        title = customtkinter.CTkLabel(
            self, text="Seleccione una opción", font=self._title_font)
        title.place(relx=0.5, rely=0.1, anchor=customtkinter.CENTER)

        self.label = CustomLabel(master=self)
        self.label.place(relx=0.5, rely=0.7, anchor=customtkinter.CENTER)

        button_load_data = customtkinter.CTkButton(
            self.label, text="Predecir datos", command=self._predict, font=self._button_font, width=150,
            height=50, corner_radius=20, fg_color="RoyalBlue3", hover_color="RoyalBlue4")
        button_load_data.place(relx=0.5, rely=0.26,
                               anchor=customtkinter.CENTER)

        button_config = customtkinter.CTkButton(
            self.label, text="Cambiar parámetros", command=self._config, font=self._button_font, width=150,
            height=50, corner_radius=20, fg_color="RoyalBlue3", hover_color="RoyalBlue4")
        button_config.place(relx=0.5, rely=0.39, anchor=customtkinter.CENTER)

        button_back_start = customtkinter.CTkButton(
            self, text="Inicio", command=self._cancel, font=self._button_font, width=150,
            height=50, corner_radius=20, fg_color="brown3", hover_color="brown4")
        button_back_start.place(relx=0.2, rely=0.9, anchor=customtkinter.E)

        button_save = customtkinter.CTkButton(
            self, text="Guardar modelo", command=self._save_model, font=self._button_font, width=150,
            height=50, corner_radius=20, fg_color="lime green", hover_color="forest green")
        button_save.place(relx=0.75, rely=0.9, anchor=customtkinter.W)

    def _config(self):
        self.controller.show_frame("HiperparametersPage")

    def _predict(self):
        self.controller.show_frame("PredictPage")

    def _save_model(self):
        directory = customtkinter.filedialog.asksaveasfilename(initialdir="./",
                                                               title="Seleccione donde guardar el fichero",
                                                               filetypes=(("Pickle files",
                                                                           "*.pkl*"),
                                                                          ("all files",
                                                                           "*.*")))

        if len(directory) > 0:
            self.logic_app.save_model(directory)

    def _cancel(self):
        AcceptWindow(master=self.master, controller=self.controller,
                     message="¿Seguro que desea volver al inicio?\n(Si no se guarda el modelo se perderá)")
        self.logic_app._has_model = False
        boolvar = customtkinter.BooleanVar(self.master, name="window_accept")
        if boolvar.get():
            self.controller.show_frame("MainPage")


class TrainingPage(CustomFrame):
    """In this page the training ocurrs
    """

    def __init__(self, logic_app, parent, controller):
        super().__init__(logic_app, parent, controller)

        self.logic_app = logic_app
        self.controller = controller

        title = customtkinter.CTkLabel(
            self, text="Ajuste los parámetros de entrenamiento", font=self._title_font)
        title.place(relx=0.5, rely=0.1, anchor=customtkinter.CENTER)

        self.label = CustomLabel(master=self)
        self.label.place(relx=0.5, rely=0.7, anchor=customtkinter.CENTER)

        self.epochs = customtkinter.IntVar(
            master=self.master, value=5, name="epochs")

        self.button_cancel = customtkinter.CTkButton(
            self, text="Cancelar", command=self._cancel, font=self._button_font, width=150,
            height=50, corner_radius=20, fg_color="brown3", hover_color="brown4", bg_color="gray17")

        self.button_create = customtkinter.CTkButton(
            self, text="Entrenar", command=self._train, font=self._button_font, width=150,
            height=50, corner_radius=20, fg_color="lime green", hover_color="forest green", bg_color="gray17")

        self.training_var = customtkinter.StringVar(
            master=self.master, value="Entrenando", name="training_var")

        self.training = customtkinter.CTkLabel(
            self.label, text=self.training_var.get(), font=self._button_font, bg_color="gray17")

        self.epochs_title = customtkinter.CTkLabel(
            self.label, text="Ajustar épocas", font=self._button_font, bg_color="gray17")

        self.slider_epochs = customtkinter.CTkSlider(
            master=self.label, from_=1, to=3000, variable=self.epochs, width=700, command=self._epochs_label)

        self.epochs_tag = customtkinter.CTkLabel(
            master=self.label, text=str(self.epochs.get()), font=self._button_font)

    def _epochs_label(self, value):
        self.epochs_tag.configure(text=str(int(value)))

    def _cancel(self):

        AcceptWindow(master=self.master, controller=self.controller,
                     message="¿Seguro que desea cancelar el entrenamiento?")
        boolvar = customtkinter.BooleanVar(self.master, name="window_accept")
        self.logic_app.model.model.summary()

        if boolvar.get():
            self.controller.show_frame("MenuSelectPage")

    def _do_train(self, config_train):

        self.logic_app.train(config_train=config_train)

    def _wait_train(self, train_th):

        while train_th.is_alive():
            time.sleep(1)
            if self.training_var.get() == "Entrenando...":
                self.training_var.set("Entrenando")
            else:
                self.training_var.set(self.training_var.get()+".")

            self.training.configure(text=self.training_var.get())

        self.controller.show_frame("ResultsPage")

    def _train(self):

        config_train = dict()
        config_train['epochs'] = self.epochs.get()
        self.epochs_title.place_forget()
        self.slider_epochs.place_forget()
        self.epochs_tag.place_forget()
        self.button_create.place_forget()
        self.button_cancel.place_forget()
        self.training.place(relx=0.5, rely=0.3,
                            anchor=customtkinter.CENTER)

        self.train_th = threading.Thread(
            target=self._do_train, args=(config_train, ), daemon=True)

        self.wait_th = threading.Thread(
            target=self._wait_train, args=(self.train_th, ), daemon=True)

        self.train_th.start()
        self.wait_th.start()

    def update_custom(self):
        self.training.place_forget()

        self.epochs_title.place(relx=0.5, rely=0.25,
                                anchor=customtkinter.CENTER)

        self.slider_epochs.place(
            relx=0.5, rely=0.3, anchor=customtkinter.CENTER)

        self.epochs_tag.place(relx=0.5, rely=0.35,
                              anchor=customtkinter.CENTER)

        self.button_create.place(relx=0.8, rely=0.9, anchor=customtkinter.W)
        self.button_cancel.place(relx=0.2, rely=0.9, anchor=customtkinter.E)


class PredictPage(CustomFrame):
    """Class for making predictions
    """

    prevPoint = [0, 0]
    currentPoint = [0, 0]

    penColor = "black"
    stroke = 1

    canvas_data = []

    shapeFill = "black"
    width = 0
    height = 0
    white = (255)
    black = (0)

    def __init__(self, logic_app, parent, controller):
        super().__init__(logic_app, parent, controller)

        self.logic_app = logic_app
        self.controller = controller

        title = customtkinter.CTkLabel(
            self, text="Introduzca los valores a predecir", font=self._title_font)
        title.place(relx=0.5, rely=0.1, anchor=customtkinter.CENTER)

        self.label = CustomLabel(master=self)
        self.label.place(relx=0.5, rely=0.7, anchor=customtkinter.CENTER)

        self.predictstr = customtkinter.StringVar(
            master=self.master, value="cero", name="preictstr")
        self.text_title = customtkinter.CTkLabel(
            self.label, text="Introducir número\n(Numeral)", font=self._button_font, bg_color="gray17")
        self.input = customtkinter.CTkEntry(
            master=self.label, textvariable=self.predictstr, width=200, font=self._button_font, justify='center')

        self.image1 = Image.new(mode="L", size=(280, 280), color=(0))
        self.draw = ImageDraw.Draw(self.image1)
        self.image_title = customtkinter.CTkLabel(
            self.label, text="Dibujar número", font=self._button_font, bg_color="gray17")
        self.canvas = customtkinter.CTkCanvas(
            self.label, height=280, width=280, bg="black")

        self.button_delete = customtkinter.CTkButton(
            self.label, text="Borrar", text_color="gray25", command=self.clearScreen, font=self._button_font, width=150,
            height=50, corner_radius=20, fg_color="gray65", hover_color="gray45", bg_color="gray17")

        self.canvas.bind("<B1-Motion>", self.paint)
        self.canvas.bind("<ButtonRelease-1>", self.paint)
        self.canvas.bind("<Button-1>", self.paint)

        button_create = customtkinter.CTkButton(
            self, text="Introducir", command=self._confirm, font=self._button_font, width=150,
            height=50, corner_radius=20, fg_color="lime green", hover_color="forest green", bg_color="gray17")
        button_create.place(relx=0.8, rely=0.9, anchor=customtkinter.W)

        button_back = customtkinter.CTkButton(
            self, text="Atrás", command=self._back, font=self._button_font, width=150,
            height=50, corner_radius=20, fg_color="brown3", hover_color="brown4", bg_color="gray17")
        button_back.place(relx=0.2, rely=0.9, anchor=customtkinter.E)

    def _confirm(self):
        params = list()

        if InputType.TEXT in self.logic_app.model.models:
            params.append(tensorflow.convert_to_tensor(
                [self.predictstr.get()], dtype="string"))

        if InputType.IMAGE in self.logic_app.model.models:

            self.image1 = self.image1.resize((28, 28))

            numpydata = np.asarray(self.image1)
            numpydata = [numpydata]
            numpydata = np.asarray(numpydata)

            numpydata = np.reshape(
                numpydata, np.append(numpydata.shape, (1)))

            numpydata = numpydata.astype('float32')
            numpydata = numpydata / 255
            params.append(numpydata)

        predicted = self.logic_app.predict_data(params)

        PredictWindow(master=self.master, controller=self.controller,
                      message="Número: " + str(predicted))

        # Clear Screen

    def clearScreen(self):
        self.canvas.delete("all")
        del self.image1
        del self.draw
        self.image1 = Image.new(mode="L", size=(280, 280), color=(0))
        self.draw = ImageDraw.Draw(self.image1)

    def paint(self, event):

        x = event.x
        y = event.y

        self.currentPoint = [x, y]

        if self.prevPoint != [0, 0]:
            self.canvas.create_line(
                self.prevPoint[0],
                self.prevPoint[1],
                self.currentPoint[0],
                self.currentPoint[1],
                width=20,
                fill="white"
            )
            self.draw.line([int(self.prevPoint[0]/1),
                            int(self.prevPoint[1]/1),
                            int(self.currentPoint[0]/1),
                            int(self.currentPoint[1]/1)], width=20, fill="white")

        self.prevPoint = self.currentPoint

        if event.type == "5":
            self.prevPoint = [0, 0]

    def _back(self):
        self.controller.show_frame("MenuSelectPage")

    def update_custom(self):
        plus = 0.5

        if InputType.IMAGE in self.logic_app.model.models:
            self.canvas.place(relx=plus, rely=0.4, anchor=customtkinter.CENTER)
            self.image_title.place(relx=plus, rely=0.17,
                                   anchor=customtkinter.CENTER)
            self.canvas.config(cursor="pencil")
            self.button_delete.place(
                relx=plus, rely=0.65, anchor=customtkinter.CENTER)
            plus -= 0.3

        if InputType.TEXT in self.logic_app.model.models:
            self.text_title.place(relx=plus, rely=0.3,
                                  anchor=customtkinter.CENTER)
            self.input.place(relx=plus, rely=0.38, anchor=customtkinter.CENTER)
            plus += 0.4


class ResultsPage(CustomFrame):
    """Frame class for the results of training
    """

    def __init__(self, logic_app, parent, controller):
        super().__init__(logic_app, parent, controller)

        self.logic_app = logic_app
        self.controller = controller

        title = customtkinter.CTkLabel(
            self, text="Resultados", font=self._title_font)
        title.place(relx=0.5, rely=0.1, anchor=customtkinter.CENTER)

        self.label = CustomLabel(master=self)
        self.label.place(relx=0.5, rely=0.7, anchor=customtkinter.CENTER)

        button_return = customtkinter.CTkButton(
            self.label, text="Volver al menu", command=self._back, font=self._button_font, width=150,
            height=50, corner_radius=20, fg_color="brown3", hover_color="brown4", bg_color="gray17")
        button_return.place(relx=0.5, rely=0.7, anchor=customtkinter.CENTER)

    def _back(self):
        self.controller.show_frame("MenuSelectPage")

    def _show_graph(self, hist, message):
        GraphWindow(master=self.master, controller=self.controller,
                    message=message, hist=hist)

    def update_custom(self):
        models = list()
        if InputType.TEXT in self.logic_app.model.models:
            models.append("texto")
        if InputType.IMAGE in self.logic_app.model.models:
            models.append("imagen")
        if InputType.AUDIO in self.logic_app.model.models:
            models.append("audio")
        sumx = 0.2
        hists_and_models = zip(self.logic_app.model.history, models)
        for hist, model in hists_and_models:
            button = customtkinter.CTkButton(
                self.label, text="Cargar modelo de "+str(model), command=lambda: self._show_graph(hist, model), font=self._button_font, width=150,
                height=50, corner_radius=20, fg_color="RoyalBlue3", hover_color="RoyalBlue4")
            button.place(relx=sumx, rely=0.35, anchor=customtkinter.CENTER)
            sumx += 0.3
