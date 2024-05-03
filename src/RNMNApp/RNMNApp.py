'''This file defines the RNMNApp Class'''

import pickle
import os
from .RNMNGuiApp import RNMNAppGui
from .InputType import InputType, ImportError
from ProcessData import ProcessData, ProcessError
from ProcessData import ProcessText
from RNMNParent import RNMNModel, RNMNParams


class RNMNApp():
    """This class start the app and get the location of the data and
      the trained model (if it exists) 
    """

    preprocessed_data_and_types: dict
    processed_data_and_types: dict
    model: RNMNModel
    app_gui: RNMNAppGui
    _no_gui: bool

    _has_model: bool

    def __init__(self, **kwargs) -> None:
        self.preprocessed_data_and_types = dict()
        self._no_gui = kwargs['gui']
        self._has_model = False

    def start_app(self):
        if self._no_gui == False:
            self.app_gui_start()
        else:
            self.app_no_gui_start()

    def get_text_data(self, directory: str):

        try:
            text = ProcessText(directory)
        except ProcessError as ex:
            raise ImportError("Error while importing text data")

        self.preprocessed_data_and_types[InputType.TEXT] = text

    def get_audio_data(self, directory: str):

        try:
            audio = ProcessData(directory)
        except ProcessError as ex:
            raise ImportError("Error while importing audio data")

        self.preprocessed_data_and_types[InputType.AUDIO] = audio

    def get_image_data(self, directory: str):
        try:
            image = ProcessData(directory)
        except ProcessError as ex:
            raise ImportError("Error while importing image data")

        self.preprocessed_data_and_types[InputType.IMAGE] = image

    def del_text_data(self):
        del self.processed_data_and_types[InputType.TEXT]
        del self.preprocessed_data_and_types[InputType.TEXT]

    def del_audio_data(self):
        del self.processed_data_and_types[InputType.AUDIO]
        del self.preprocessed_data_and_types[InputType.AUDIO]

    def del_image_data(self):
        del self.processed_data_and_types[InputType.IMAGE]
        del self.preprocessed_data_and_types[InputType.IMAGE]

    def create_model(self, params_dict):
        self.model = RNMNModel(params_dict=params_dict)

    def save_model(self, directory: str):
        with open(directory, 'wb') as output:
            pickle.dump(self.model, output, pickle.HIGHEST_PROTOCOL)

    def load_model(self, directory: str):
        with open(directory, 'rb') as input:
            try:
                self.model = pickle.load(input)
            except pickle.UnpicklingError as ex:
                raise ImportError("Error while importing model")
            else:
                self._has_model = True

    def preprocess_typedata_data(self, list_types):
        self.processed_data_and_types = dict()

        for k in list_types:
            try:
                self.preprocessed_data_and_types[k].process()
            except ProcessError:
                raise ImportError("Error on process data")
            else:
                self.processed_data_and_types[k] = self.preprocessed_data_and_types[k].data_processed

    def preprocess_all_data(self):
        self.processed_data_and_types = dict()

        for k in self.preprocessed_data_and_types.keys():

            try:
                self.preprocessed_data_and_types[k].process()
            except ProcessError:
                raise ImportError("Error on process data")
            else:
                self.processed_data_and_types[k] = self.preprocessed_data_and_types[k].data_processed

    def add_data_to_model(self):
        
        for k in self.processed_data_and_types.keys():
            if k == InputType.TEXT:
                self.model.add_data_text_model(self.processed_data_and_types[k])

            if k == InputType.AUDIO:
                self.model.add_data_audio_model(self.processed_data_and_types[k])
        
            if k == InputType.IMAGE:
                self.model.add_data_image_model(self.processed_data_and_types[k])

            
                
    def compile_model(self, parameters):
        self.model.compile_model(parameters)
        self._has_model = True
    

    def app_no_gui_start(self):
        print("\nPorfavor seleccione una opción:\n\n\t1-Crear modelo\n\t2-Cargar modelo")
        sel = input("\nIntroduzca la opción: ")

        while sel != "1" and sel != "2":
            print(
                "\n\n\nOpción no válida seleccione una opción:\n\n\t1-Crear modelo\n\t2-Cargar modelo")
            sel = input("\nIntroduzca la opción: ")

        match sel:
            case "1":
                self.app_no_gui_model_creation()
            case "2":
                print(
                    "\n\nTenga en cuenta que se dirige la ruta desde el directorio de ejecución")
                dir = input("\nIntroduzca el directorio: ")

                while not os.path.exists(dir):
                    while not os.path.exists(dir):
                        dir = input(
                            "\n\nError, el fichero no existe o no es un .pkl: ")
                    try:
                        self.load_model(dir)
                    except pickle.UnpicklingError:
                        dir = "test.pkl"

    def app_no_gui_model_creation(self):

        def _layer_ask(params_dict, layer_name):
            params_dict['layer_'+layer_name] = dict()
            params_dict['layer_'+layer_name]['num_neurons'] = input(
                "\n\nIntroduzca el número de neuronas de la capa " + layer_name+": ")
            while (params_dict['layer_'+layer_name]['num_neurons'].isnumeric() and int(params_dict['layer_'+layer_name]['num_neurons']) <= 0) or not params_dict['layer_'+layer_name]['num_neurons'].isnumeric():
                params_dict['num_inputs'] = input(
                    "Opción no válida, introduzca un número positivo mayor que 0: ")
            cont = 1
            print("\n\n")

            activations = [act.value for act in RNMNParams.RNMNActivations]
            for act in activations:
                print(str(cont) + "- " + act)
                cont += 1
            params_dict['layer_'+layer_name]['activation'] = input(
                "\n\nIntroduzca el tipo de activación (1-"+str(cont)+") de la capa " + layer_name+": ")
            while (params_dict['layer_'+layer_name]['activation'].isnumeric() and (int(params_dict['layer_'+layer_name]['activation']) <= 0 or int(params_dict['layer_'+layer_name]['activation']) > cont)) or not params_dict['layer_'+layer_name]['activation'].isnumeric():
                print("\n\n")
                for act in activations:
                    print(str(cont) + "- " + act)
                    cont += 1
                params_dict['layer_'+layer_name]['activation'] = input(
                    "Opción no válida, introduzca un número de las opciones mostradas: ")
                
            params_dict['layer_'+layer_name]['activation'] = activations[int(params_dict['layer_'+layer_name]['activation']) - 1]

        models = [('texto', "text"), ("audio", "audio"), ("imagen", "image")]

        params_dict = dict()
        for model, model_ing in models:
            sel = input("\n\nDesea modelo de " + model + " (Y/n): ")
            sel = sel.lower()
            while sel != "y" and sel != "n":
                sel = input("Opción no válida, introduzca Y (Yes) o n (no): ")
                sel = sel.lower()

            if sel.lower() == "y":
                params_dict[model_ing+"_config"] = dict()
                sel = input(
                    "\n\n¿Desea cargar los ajustes predeterminados? (Y/n): ")
                sel = sel.lower()
                while sel != "y" and sel != "n":
                    sel = input(
                        "Opción no válida, introduzca Y (Yes) o n (no): ")
                    sel = sel.lower()

                if sel.lower() == "y":
                    pass  # TO-DO ajustes predeterminados
                else:
                    params_dict[model_ing+"_config"]['num_inputs'] = input(
                        "\n\nIntroduzca el número de neuronas (D para default): ")
                    while (params_dict[model_ing+"_config"]['num_inputs'].isnumeric() and int(params_dict[model_ing+"_config"]['num_inputs']) <= 0) or (not params_dict[model_ing+"_config"]['num_inputs'].isnumeric() and params_dict[model_ing+"_config"]['num_inputs'].lower() != 'd'):
                        params_dict['num_inputs'] = input(
                            "Opción no válida, introduzca un número positivo mayor que 0 o 'd' para que las detecte el programa: ")

                    params_dict[model_ing+"_config"]['num_layers'] = input(
                        "\n\nIntroduzca el número de capas ocultas: ")
                    while (params_dict[model_ing+"_config"]['num_layers'].isnumeric() and int(params_dict[model_ing+"_config"]['num_layers']) < 0) or not params_dict[model_ing+"_config"]['num_layers'].isnumeric():
                        params_dict[model_ing+"_config"]['num_layers'] = input(
                            "Opción no válida, introduzca un número positivo: ")
                    
                    params_dict[model_ing+"_config"]['layers_dict'] = dict()

                    for i in range(1, int(params_dict[model_ing+"_config"]['num_layers']) + 1):
                        _layer_ask(params_dict[model_ing+"_config"]['layers_dict'], str(i))

                    _layer_ask(params_dict[model_ing+"_config"]['layers_dict'], "out")

        self.create_model(params_dict)

    def app_gui_start(self):
        self.app_gui = RNMNAppGui(self)

        self.app_gui.mainloop()
