'''This file defines the RNMNAppGui Class'''

import tkinter
import customtkinter
from RNMNApp import RNMNApp
from .RNMNGuiWindows import AcceptWindow, ErrorWindow
from ..InputType import ImportError, InputType
from .RNMNGuiTabs import CreateNetTabView, ValidationTabError
from .RNMNGuiLabels import CustomLabel
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

    def update(self):
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
        self.rely = dict()

        title = customtkinter.CTkLabel(
            self, text="Seleccione datos a subir", font=self._title_font)
        title.place(relx=0.5, rely=0.1, anchor=customtkinter.CENTER)

        self.label = CustomLabel(master=self)
        self.label.place(relx=0.5, rely=0.7, anchor=customtkinter.CENTER)

        self.rely = {"text": 0, "audio": 0, "image": 0}

        button_cancel = customtkinter.CTkButton(
            self, text="Cancelar", command=self._cancel, font=self._button_font, width=150,
            height=50, corner_radius=20, fg_color="brown3", hover_color="brown4")
        button_cancel.place(relx=0.2, rely=0.9, anchor=customtkinter.E)

        button_accept = customtkinter.CTkButton(
            self, text="Aceptar", command=self._accept, font=self._button_font, width=150,
            height=50, corner_radius=20, fg_color="lime green", hover_color="forest green")
        button_accept.place(relx=0.8, rely=0.9, anchor=customtkinter.W)

    def add_text_button(self):
        self._text_data = customtkinter.CTkLabel(
            self.label, text="Datos de texto añadidos correctamente", font=self._button_font)
        self._button_text_recover = customtkinter.CTkButton(self.label, text="Eliminar datos de texto",
                                                            command=self._recover_text_button, font=self._button_font, width=150,
                                                            height=50, corner_radius=20, fg_color="brown3", hover_color="brown4")

        self._button_text = customtkinter.CTkButton(
            self.label, text="Cargar datos de texto", command=self._load_text_data, font=self._button_font, width=150,
            height=50, corner_radius=20, fg_color="RoyalBlue3", hover_color="RoyalBlue4")
        self._button_text.place(relx=0.5, rely=self.rely['text'],
                                anchor=customtkinter.CENTER)

    def add_audio_button(self):
        self._audio_data = customtkinter.CTkLabel(
            self.label, text="Datos de audio añadidos correctamente", font=self._button_font)
        self._button_audio_recover = customtkinter.CTkButton(self.label, text="Eliminar datos de audio",
                                                             command=self._recover_audio_button, font=self._button_font, width=150,
                                                             height=50, corner_radius=20, fg_color="brown3", hover_color="brown4")

        self._button_audio = customtkinter.CTkButton(
            self.label, text="Cargar datos de audio", command=self._load_audio_data, font=self._button_font, width=150,
            height=50, corner_radius=20, fg_color="RoyalBlue3", hover_color="RoyalBlue4")
        self._button_audio.place(
            relx=0.5, rely=self.rely['audio'], anchor=customtkinter.CENTER)

    def add_image_button(self):
        self._image_data = customtkinter.CTkLabel(
            self.label, text="Datos de imagen añadidos correctamente", font=self._button_font)
        self._button_image_recover = customtkinter.CTkButton(self.label, text="Eliminar datos de imagen",
                                                             command=self._recover_image_button, font=self._button_font, width=150,
                                                             height=50, corner_radius=20, fg_color="brown3", hover_color="brown4")
        self._button_image = customtkinter.CTkButton(
            self.label, text="Cargar datos de imagen", command=self._load_image_data, font=self._button_font, width=150,
            height=50, corner_radius=20, fg_color="RoyalBlue3", hover_color="RoyalBlue4")
        self._button_image.place(
            relx=0.5, rely=self.rely['image'], anchor=customtkinter.CENTER)

    def _recover_text_button(self):
        self._text_data.place_forget()
        self._button_text_recover.place_forget()
        self._button_text.place(relx=0.5, rely=self.rely['text'],
                                anchor=customtkinter.CENTER)
        self.logic_app.del_text_data()
        self._data_counter -= 1
        self._data_to_clear.remove(self._recover_text_button)

    def _recover_audio_button(self):
        self._audio_data.place_forget()
        self._button_audio_recover.place_forget()
        self._button_audio.place(relx=0.5, rely=self.rely['audio'],
                                 anchor=customtkinter.CENTER)
        self.logic_app.del_audio_data()
        self._data_counter -= 1
        self._data_to_clear.remove(self._recover_audio_button)

    def _recover_image_button(self):
        self._image_data.place_forget()
        self._button_image_recover.place_forget()
        self._button_image.place(
            relx=0.5, rely=self.rely['image'], anchor=customtkinter.CENTER)
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
                        relx=0.5, rely=self.rely['text'], anchor=customtkinter.E)
                    self._button_text_recover.place(
                        relx=0.55, rely=self.rely['text'], anchor=customtkinter.W)
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
                        relx=0.5, rely=self.rely['audio'], anchor=customtkinter.E)
                    self._button_audio_recover.place(
                        relx=0.55, rely=self.rely['audio'], anchor=customtkinter.W)
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
            for fun in self._data_to_clear.copy():
                fun()

            if self.logic_app._has_model:
                self.controller.show_frame("MenuSelectPage")
            else:
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
                self.logic_app.add_data_to_model()
                if self.logic_app._has_model:
                    self.controller.show_frame("MenuSelectPage")
                else:
                    self.controller.show_frame("HiperparametersPage")

    def update(self):

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
            self.add_text_button()

        if self.controller.models['audio']:
            rel_sum += rel
            self.rely['audio'] = rel_sum
            self.add_audio_button()

        if self.controller.models['image']:
            rel_sum += rel
            self.rely['image'] = rel_sum
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

        self.controller.models['text'] = var_text.get()

        self.controller.models['audio'] = var_audio.get()
        self.controller.models['image'] = var_image.get()

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
                        message="Porfavor introduzca un valor numérico superior a 0 en el número de entradas y salidas")
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
            height=50, corner_radius=20, fg_color="brown3", hover_color="brown4")
        button_cancel.place(relx=0.2, rely=0.9, anchor=customtkinter.E)

        button_create = customtkinter.CTkButton(
            self, text="Confirmar", command=self._confirm, font=self._button_font, width=150,
            height=50, corner_radius=20, fg_color="lime green", hover_color="forest green")
        button_create.place(relx=0.8, rely=0.9, anchor=customtkinter.W)

    def model_frame_create(self):

        optimizer_var: customtkinter.StringVar
        loss_var: customtkinter.StringVar
        title: str

        title = customtkinter.CTkLabel(
            self.label, text="Ajustar losses", font=self._button_font)
        title.place(relx=0.2, rely=0.25, anchor=customtkinter.CENTER)
        loss_var = customtkinter.StringVar(
            master=self.master, value=self.losses[0], name="loss")
        combobox_loss = customtkinter.CTkComboBox(master=self.label, values=self.losses,
                                                  state="readonly",
                                                  variable=loss_var, width=153)
        combobox_loss.place(relx=0.35, rely=0.25, anchor=customtkinter.CENTER)

        title = customtkinter.CTkLabel(
            master=self.label, text="Ajustar optimizer", font=self._button_font)
        title.place(relx=0.2, rely=0.35, anchor=customtkinter.CENTER)
        optimizer_var = customtkinter.StringVar(
            master=self.master, value=self.optimizers[0], name="optimizer")
        combobox_optimizer = customtkinter.CTkComboBox(master=self.label, values=self.optimizers,
                                                       state="readonly",
                                                       variable=optimizer_var, width=100)
        combobox_optimizer.place(
            relx=0.35, rely=0.35, anchor=customtkinter.CENTER)

        title = customtkinter.CTkLabel(
            master=self.label, text="Seleccionar las métricas deseadas", font=self._button_font)
        title.place(relx=0.63, rely=0.1, anchor=customtkinter.CENTER)

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
                                                variable=check_var, onvalue=True, offvalue=False)

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

        aux_dict['metrics'] = RNMNParams.RNMNMetricsTraduction.translate(
            metrics)

        return aux_dict

    def _confirm(self):

        params_dict = self._get_params()

        self.logic_app.compile_model(params_dict)

        self.controller.show_frame("MenuSelectPage")

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
            self.label, text="Entrenar red", command=self._train, font=self._button_font, width=150,
            height=50, corner_radius=20, fg_color="RoyalBlue3", hover_color="RoyalBlue4")
        button_load_data.place(relx=0.5, rely=0.13, anchor=customtkinter.CENTER)

        button_load_data = customtkinter.CTkButton(
            self.label, text="Predecir datos", command=self._predict, font=self._button_font, width=150,
            height=50, corner_radius=20, fg_color="RoyalBlue3", hover_color="RoyalBlue4")
        button_load_data.place(relx=0.5, rely=0.26, anchor=customtkinter.CENTER)

        button_config = customtkinter.CTkButton(
            self.label, text="Cambiar parámetros", command=self._config, font=self._button_font, width=150,
            height=50, corner_radius=20, fg_color="RoyalBlue3", hover_color="RoyalBlue4")
        button_config.place(relx=0.5, rely=0.39, anchor=customtkinter.CENTER)

        button_load_data = customtkinter.CTkButton(
            self.label, text="Cargar otros datos", command=self._new_data, font=self._button_font, width=150,
            height=50, corner_radius=20, fg_color="RoyalBlue3", hover_color="RoyalBlue4")
        button_load_data.place(relx=0.5, rely=0.52, anchor=customtkinter.CENTER)

        button_cancel = customtkinter.CTkButton(
            self, text="Menú", command=self._cancel, font=self._button_font, width=150,
            height=50, corner_radius=20, fg_color="brown3", hover_color="brown4")
        button_cancel.place(relx=0.5, rely=0.9, anchor=customtkinter.CENTER)


    def _config(self):
        self.controller.show_frame("HiperparametersPage")

    def _new_data(self):
        self.controller.show_frame("SelectDataPage")

    def _predict(self):

        self.logic_app.predict_data()
        self.controller.show_frame("ResultsPage")

    def _train(self):
        self.controller.show_frame("TrainingPage")

        
    def _cancel(self):
        AcceptWindow(master=self.master, controller=self.controller,
                     message="¿Seguro que desea volver al menú?\n(Si no se guarda el modelo se perderá)")
        boolvar = customtkinter.BooleanVar(self.master, name="window_accept")
        if boolvar.get():
            self.controller.show_frame("MainPage")


class TrainingPage(CustomFrame):

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
            master=self.master, value=100, name="epochs")

        button_cancel = customtkinter.CTkButton(
            self, text="Cancelar", command=self._back, font=self._button_font, width=150,
            height=50, corner_radius=20, fg_color="brown3", hover_color="brown4")
        button_cancel.place(relx=0.2, rely=0.9, anchor=customtkinter.E)

        button_create = customtkinter.CTkButton(
            self, text="Entrenar", command=self._train, font=self._button_font, width=150,
            height=50, corner_radius=20, fg_color="lime green", hover_color="forest green")
        button_create.place(relx=0.8, rely=0.9, anchor=customtkinter.W)

        self.training = customtkinter.CTkLabel(
            self.label, text="Entrenando...", font=self._button_font)
                
        self.epochs_title = customtkinter.CTkLabel(
            self.label, text="Ajustar épocas", font=self._button_font)

        self.slider_epochs = customtkinter.CTkSlider(
            master=self.label, from_=1, to=5000, variable=self.epochs, width=700, command=self._epochs_label)
        
        self.epochs_tag = customtkinter.CTkLabel(
            master=self.label, text=str(self.epochs.get()), font=self._button_font)
        
    def _epochs_label(self, value):
        self.epochs_tag.configure(text=str(int(value)))

    def _back(self):
        self.controller.show_frame("MenuSelectPage")

    def _train(self):

        AcceptWindow(master=self.master, controller=self.controller,
                     message="¿Seguro que desea entrenar el modelo?")
        boolvar = customtkinter.BooleanVar(self.master, name="window_accept")
        if boolvar.get():
            self.controller.show_frame("MainPage")
        config_train = dict()
        config_train['epochs'] = self.epochs.get()

        self.epochs_title.place_forget()
        self.slider_epochs.place_forget()
        self.epochs_tag.place_forget()

        self.training.place(relx=0.5, rely=0.3, anchor=customtkinter.CENTER)
        self.training.update()

        self.logic_app.model.train(config_train)

        self.controller.show_frame("ResultsPage")

    
    def update(self):
        self.training.place_forget()

        self.epochs_title.place(relx=0.5, rely=0.25, anchor=customtkinter.CENTER)

        self.slider_epochs.place(relx=0.5, rely=0.3, anchor=customtkinter.CENTER)

        self.epochs_tag.place(relx=0.5, rely=0.35,
                              anchor=customtkinter.CENTER)
        



class ResultsPage(CustomFrame):

    def __init__(self, logic_app, parent, controller):
        super().__init__(logic_app, parent, controller)

        self.logic_app = logic_app
        self.controller = controller

        title = customtkinter.CTkLabel(
            self, text="Resultados", font=self._title_font)
        title.place(relx=0.5, rely=0.1, anchor=customtkinter.CENTER)

        self.label = CustomLabel(master=self)
        self.label.place(relx=0.5, rely=0.7, anchor=customtkinter.CENTER)

        
        button_cancel = customtkinter.CTkButton(
            self, text="Volver al menu", command=self._back, font=self._button_font, width=150,
            height=50, corner_radius=20, fg_color="brown3", hover_color="brown4")
        button_cancel.place(relx=0.2, rely=0.9, anchor=customtkinter.E)

    def _back(self):
        self.controller.show_frame("MenuSelectPage")

