'''This file defines the RNMNAppGui Class'''

import tkinter
import customtkinter
from RNMNApp import RNMNApp
from .RNMNGuiWindows import AcceptWindow, ErrorWindow
from ..InputType import ImportError, InputType
from .RNMNGuiTabs import CreateNetTabView, ModifyHPNetTabView, ValidationTabError
from RNMNParent import RNMNParams


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

    def clean(self):
        pass


class MainPage(CustomFrame):

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

    def _create_model(self):
        self.controller.show_frame("CreateModelPage")

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

        title = customtkinter.CTkLabel(
            self, text="Seleccione datos a subir", font=self._title_font)
        title.place(relx=0.5, rely=0.2, anchor=customtkinter.CENTER)

        self._text_data = title = customtkinter.CTkLabel(
            self, text="Datos de texto añadidos correctamente", font=self._button_font)
        self._button_text_recover = customtkinter.CTkButton(self, text="Eliminar datos de texto",
                                                            command=self._recover_text_button, font=self._button_font, width=150,
                                                            height=50, corner_radius=20, fg_color="brown3", hover_color="brown4")

        self._button_text = customtkinter.CTkButton(
            self, text="Cargar datos de texto", command=self._load_text_data, font=self._button_font, width=150,
            height=50, corner_radius=20, fg_color="RoyalBlue3", hover_color="RoyalBlue4")
        self._button_text.place(relx=0.5, rely=0.35,
                                anchor=customtkinter.CENTER)

        self._audio_data = title = customtkinter.CTkLabel(
            self, text="Datos de audio añadidos correctamente", font=self._button_font)
        self._button_audio_recover = customtkinter.CTkButton(self, text="Eliminar datos de audio",
                                                             command=self._recover_audio_button, font=self._button_font, width=150,
                                                             height=50, corner_radius=20, fg_color="brown3", hover_color="brown4")

        self._button_audio = customtkinter.CTkButton(
            self, text="Cargar datos de audio", command=self._load_audio_data, font=self._button_font, width=150,
            height=50, corner_radius=20, fg_color="RoyalBlue3", hover_color="RoyalBlue4")
        self._button_audio.place(
            relx=0.5, rely=0.48, anchor=customtkinter.CENTER)

        self._image_data = title = customtkinter.CTkLabel(
            self, text="Datos de imagen añadidos correctamente", font=self._button_font)
        self._button_image_recover = customtkinter.CTkButton(self, text="Eliminar datos de imagen",
                                                             command=self._recover_image_button, font=self._button_font, width=150,
                                                             height=50, corner_radius=20, fg_color="brown3", hover_color="brown4")
        self._button_image = customtkinter.CTkButton(
            self, text="Cargar datos de imagen", command=self._load_image_data, font=self._button_font, width=150,
            height=50, corner_radius=20, fg_color="RoyalBlue3", hover_color="RoyalBlue4")
        self._button_image.place(
            relx=0.5, rely=0.61, anchor=customtkinter.CENTER)

        button_cancel = customtkinter.CTkButton(
            self, text="Cancelar", command=self._cancel, font=self._button_font, width=150,
            height=50, corner_radius=20, fg_color="brown3", hover_color="brown4")
        button_cancel.place(relx=0.45, rely=0.8, anchor=customtkinter.E)

        button_accept = customtkinter.CTkButton(
            self, text="Aceptar", command=self._accept, font=self._button_font, width=150,
            height=50, corner_radius=20, fg_color="lime green", hover_color="forest green")
        button_accept.place(relx=0.55, rely=0.8, anchor=customtkinter.W)

    def _recover_text_button(self):
        self._text_data.place_forget()
        self._button_text_recover.place_forget()
        self._button_text.place(relx=0.5, rely=0.35,
                                anchor=customtkinter.CENTER)
        self.logic_app.del_text_data()
        self._data_counter -= 1
        self._data_to_clear.remove(self._recover_text_button)

    def _recover_audio_button(self):
        self._audio_data.place_forget()
        self._button_audio_recover.place_forget()
        self._button_audio.place(relx=0.5, rely=0.48,
                                 anchor=customtkinter.CENTER)
        self.logic_app.del_audio_data()
        self._data_counter -= 1
        self._data_to_clear.remove(self._recover_audio_button)

    def _recover_image_button(self):
        self._image_data.place_forget()
        self._button_image_recover.place_forget()
        self._button_image.place(
            relx=0.5, rely=0.61, anchor=customtkinter.CENTER)
        self.logic_app.del_image_data()
        self._data_counter -= 1
        self._data_to_clear.remove(self._recover_image_button)

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
                else:
                    self._button_text.place_forget()
                    self._text_data.place(
                        relx=0.5, rely=0.35, anchor=customtkinter.E)
                    self._button_text_recover.place(
                        relx=0.55, rely=0.35, anchor=customtkinter.W)
                    self._data_counter += 1
                    self._data_to_clear.add(self._recover_text_button)

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
                else:
                    self._button_audio.place_forget()
                    self._audio_data.place(
                        relx=0.5, rely=0.48, anchor=customtkinter.E)
                    self._button_audio_recover.place(
                        relx=0.55, rely=0.48, anchor=customtkinter.W)
                    self._data_counter += 1
                    self._data_to_clear.add(self._recover_audio_button)

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
                else:
                    self._button_image.place_forget()
                    self._image_data.place(
                        relx=0.5, rely=0.61, anchor=customtkinter.E)
                    self._button_image_recover.place(
                        relx=0.55, rely=0.61, anchor=customtkinter.W)
                    self._data_counter += 1
                    self._data_to_clear.add(self._recover_image_button)

    def _cancel(self):
        AcceptWindow(master=self.master, controller=self.controller,
                     message="¿Seguro que desea cancelar la carga de datos?")
        boolvar = customtkinter.BooleanVar(self.master, name="window_accept")
        if boolvar.get():
            for fun in self._data_to_clear.copy():
                fun()
            self.controller.show_frame("MainPage")

    def _accept(self):

        if self._data_counter < 1:
            ErrorWindow(master=self.master, controller=self.controller,
                        message="Añada al menos un tipo de datos, porfavor")

        else:
            AcceptWindow(master=self.master, controller=self.controller,
                         message="¿Seguro que desea proceder con estos datos?")
            boolvar = customtkinter.BooleanVar(
                self.master, name="window_accept")

            if boolvar.get():
                self.controller.show_frame("HiperparametersPage") # TO-DO cambiar a SelectPage


class CreateModelPage(CustomFrame):

    def __init__(self, logic_app, parent, controller):
        super().__init__(logic_app, parent, controller)
        self.logic_app = logic_app
        self.controller = controller

        title = customtkinter.CTkLabel(
            master=self, text="Creación de la red", font=self._title_font)
        title.place(relx=0.5, rely=0.1, anchor=customtkinter.CENTER)

        self.tab_view = CreateNetTabView(master=self, width=1080, height=720)
        self.tab_view.place(relx=0.5, rely=0.7, anchor=customtkinter.CENTER)

        button_cancel = customtkinter.CTkButton(
            self, text="Cancelar", command=self._cancel, font=self._button_font, width=150,
            height=50, corner_radius=20, fg_color="brown3", hover_color="brown4")
        button_cancel.place(relx=0.2, rely=0.9, anchor=customtkinter.E)

        button_create = customtkinter.CTkButton(
            self, text="Crear", command=self._create, font=self._button_font, width=150,
            height=50, corner_radius=20, fg_color="lime green", hover_color="forest green")
        button_create.place(relx=0.8, rely=0.9, anchor=customtkinter.W)

       

    def _get_params(self, model_name: InputType) -> dict:


        try:
            self.tab_view.validate()
        except ValidationTabError:
            raise ValidationTabError("Error on input parameters")
        else:

            params_dict = customtkinter.Variable(master=self, name="params_dict")
            print(params_dict.get())
            aux_dict = dict()
            loss = customtkinter.StringVar(
                master=self.master, name="loss_"+model_name)

            aux_dict['loss'] = loss.get()

            optimizer = customtkinter.StringVar(
                master=self.master, name="optimizer_"+model_name)

            aux_dict['optimizer'] = optimizer.get()
            metrics_names = [(metric.value) for metric in RNMNParams.RNMNMetrics]

            metrics = list()
            

            for metric in metrics_names:
                metric_var =  customtkinter.BooleanVar(
                    master=self.master,name=metric+"_"+model_name)
                if metric_var.get():
                    metrics.append(metric)

            aux_dict['metrics'] = RNMNParams.RNMNMetricsTraduction.translate(metrics)

            return aux_dict

    def _create(self):

        params_dict = {}

        var_text = customtkinter.BooleanVar(
            master=self.master, name="switch_texto")

        var_audio = customtkinter.BooleanVar(
            master=self.master, name="switch_audio")

        var_image = customtkinter.BooleanVar(
            master=self.master, name="switch_imagen")

        number_of_models = 0
        try:
            if var_text.get():
                number_of_models += 1
                params_dict['text_config'] = self._get_params("texto")

            if var_audio.get():
                number_of_models += 1
                params_dict['audio_config'] = self._get_params("audio")

            if var_image.get():
                number_of_models += 1
                params_dict['image_config'] = self._get_params("imgaen")
        except ValidationTabError:
            ErrorWindow(master=self.master, controller=self.controller,
                        message="Porfavor introduzca un valor numérico en el número de entradas y salidas")
        else:
            if number_of_models == 0:
                ErrorWindow(master=self.master, controller=self.controller,
                            message="Porfavor elija al menos un modelo")
            else:
                self.logic_app.create_model(params_dict)

                self.controller.show_frame("SelectDataPage")

    def _cancel(self):
        AcceptWindow(master=self.master, controller=self.controller,
                     message="¿Seguro que desea cancelar la creación del modelo?")
        boolvar = customtkinter.BooleanVar(self.master, name="window_accept")
        if boolvar.get():
            self.controller.show_frame("MainPage")



class HiperparametersPage(CustomFrame):

    def __init__(self, logic_app, parent, controller):
        super().__init__(logic_app, parent, controller)

        self.logic_app = logic_app
        self.controller = controller

        title = customtkinter.CTkLabel(
            self, text="Creación de la red", font=self._title_font)
        title.place(relx=0.5, rely=0.1, anchor=customtkinter.CENTER)

       

    def _get_params(self, model_name: InputType) -> dict:
        aux_dict = dict()

        loss = customtkinter.StringVar(
            master=self.master, name="loss_"+model_name)

        aux_dict['loss'] = loss.get()

        print(model_name)
        print(loss.get())

        optimizer = customtkinter.StringVar(
            master=self.master, name="optimizer_"+model_name)

        aux_dict['optimizer'] = optimizer.get()

        print(optimizer.get())
        print("")

        metrics_names = [(metric.value) for metric in RNMNParams.RNMNMetrics]

        metrics = list()
        

        for metric in metrics_names:
            metric_var =  customtkinter.BooleanVar(
                master=self.master,name=metric+"_"+model_name)
            if metric_var.get():
                metrics.append(metric)

        aux_dict['metrics'] = RNMNParams.RNMNMetricsTraduction.translate(metrics)

        return aux_dict

    def _confirm(self):

        params_dict = {}

        var_text = customtkinter.BooleanVar(
            master=self.master, name="switch_texto")

        var_audio = customtkinter.BooleanVar(
            master=self.master, name="switch_audio")

        var_image = customtkinter.BooleanVar(
            master=self.master, name="switch_imagen")

        number_of_models = 0

        if var_text.get():
            number_of_models += 1
            params_dict['text_config'] = self._get_params("texto")

        if var_audio.get():
            number_of_models += 1
            params_dict['audio_config'] = self._get_params("audio")

        if var_image.get():
            number_of_models += 1
            params_dict['image_config'] = self._get_params("imgaen")


        self.logic_app.create_model(params_dict)

        self.controller.show_frame("MainPage")

    def _cancel(self):
        AcceptWindow(master=self.master, controller=self.controller,
                     message="¿Seguro que desea cancelar la creación del modelo?")
        boolvar = customtkinter.BooleanVar(self.master, name="window_accept")
        if boolvar.get():
            self.controller.show_frame("MainPage")

    def clean(self):
        self.tab_view = ModifyHPNetTabView(master=self, width=1080, height=720)
        self.tab_view.place(relx=0.5, rely=0.7, anchor=customtkinter.CENTER)

        button_cancel = customtkinter.CTkButton(
            self, text="Cancelar", command=self._cancel, font=self._button_font, width=150,
            height=50, corner_radius=20, fg_color="brown3", hover_color="brown4")
        button_cancel.place(relx=0.2, rely=0.9, anchor=customtkinter.E)

        button_create = customtkinter.CTkButton(
            self, text="Confirmar", command=self._confirm, font=self._button_font, width=150,
            height=50, corner_radius=20, fg_color="lime green", hover_color="forest green")
        button_create.place(relx=0.8, rely=0.9, anchor=customtkinter.W)



class MenuSelectPage(CustomFrame):

    def __init__(self, logic_app, parent, controller):
        super().__init__(logic_app, parent, controller)

        self.logic_app = logic_app
        self.controller = controller

        title = customtkinter.CTkLabel(
            self, text="Seleccione una opción", font=self._title_font)
        title.place(relx=0.5, rely=0.3, anchor=customtkinter.CENTER)

    def _config(self):
        self.controller.show_frame("HiperparametersPage")

    def _new_data(self):
        self.controller.show_frame("SelectDataPage")

    def _predict(self):
        self.controller.show_frame("ResultsPage")

    def _train(self):
        self.controller.show_frame("ResultsPage")


class ResultsPage(CustomFrame):

    def __init__(self, logic_app, parent, controller):
        super().__init__(logic_app, parent, controller)

        self.logic_app = logic_app
        self.controller = controller

        title = customtkinter.CTkLabel(
            self, text="Resultados", font=self._title_font)
        title.place(relx=0.5, rely=0.3, anchor=customtkinter.CENTER)

    def _back(self):
        self.controller.show_frame("MenuSelectPage")
