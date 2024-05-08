import customtkinter
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from RNMNParent import RNMNParams


class CustomWindow(customtkinter.CTkToplevel):

    _title_font = ("Times", 20, 'bold')
    _button_font = ("Times", 20, )

    def __init__(self, master, controller: customtkinter.CTk, message, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.master = master
        self.controller = controller
        self.message = message
        self.focus_set()
        self.resizable(width=False, height=False)

    @staticmethod
    def center_window(window, width: int, height: int, scale_factor: float = 1.0):
        '''Centers the window
        '''
        screen_wth = window.winfo_screenwidth()
        screen_hgt = window.winfo_screenheight()

        x = int(((screen_wth/2) - (width/2)) * scale_factor)
        y = int(((screen_hgt/2) - (height/1.5)) * scale_factor)

        return f"{width}x{height}+{x}+{y}"

    def _accept(self):
        self.master.setvar(name="window_accept", value=True)
        self.destroy()

    def _block_on_window(self):
        self.wait_visibility()
        self.transient(self.master)
        self.grab_set()
        self.focus_force()
        self.master.wait_variable(name="window_accept")


class ErrorWindow(CustomWindow):

    def __init__(self,  master, controller: customtkinter.CTk, message, *args, **kwargs):
        super().__init__(master, controller, message, *args, **kwargs)

        self.geometry(CustomWindow.center_window(
            self, 720, 250, self._get_window_scaling()))
        self.title("Error")

        label = customtkinter.CTkLabel(
            self, text=message, font=self._title_font)
        label.place(relx=0.5, rely=0.25, anchor=customtkinter.CENTER)

        button = customtkinter.CTkButton(
            self, text="Aceptar", command=self._accept, width=150,
            height=50, corner_radius=20, fg_color="brown3", hover_color="brown4")
        button.place(relx=0.5, rely=0.6, anchor=customtkinter.CENTER)

        self._block_on_window()


class AcceptWindow(CustomWindow):

    def __init__(self,  master, controller: customtkinter.CTk, message, *args, **kwargs):
        super().__init__(master, controller, message, *args, **kwargs)

        self.geometry(CustomWindow.center_window(
            self, 720, 250, self._get_window_scaling()))
        self.title("Confirmación")

        label = customtkinter.CTkLabel(
            self, text=message, font=self._title_font)
        label.place(relx=0.5, rely=0.25, anchor=customtkinter.CENTER)

        button_cancel = customtkinter.CTkButton(
            self, text="Cancelar", command=self._cancel, font=self._button_font, width=150,
            height=50, corner_radius=20, fg_color="brown3", hover_color="brown4")
        button_cancel.place(relx=0.45, rely=0.6, anchor=customtkinter.E)

        button_accept = customtkinter.CTkButton(
            self, text="Aceptar", command=self._accept, font=self._button_font, width=150,
            height=50, corner_radius=20, fg_color="lime green", hover_color="forest green")
        button_accept.place(relx=0.55, rely=0.6, anchor=customtkinter.W)

        self._block_on_window()

    def _cancel(self):
        self.master.setvar(name="window_accept", value=False)
        self.destroy()


class PredictWindow(CustomWindow):

    _title_font = ("Times", 25, 'bold')

    def __init__(self,  master, controller: customtkinter.CTk, message, *args, **kwargs):
        super().__init__(master, controller, message, *args, **kwargs)

        self.geometry(CustomWindow.center_window(
            self, 720, 250, self._get_window_scaling()))
        self.title("Predicción")

        label = customtkinter.CTkLabel(
            self, text=message, font=self._title_font)
        label.place(relx=0.5, rely=0.25, anchor=customtkinter.CENTER)

        button = customtkinter.CTkButton(
            self, text="Aceptar", command=self._accept, width=150,
            height=50, corner_radius=20, fg_color="lime green", hover_color="forest green")
        button.place(relx=0.5, rely=0.6, anchor=customtkinter.CENTER)
        self._block_on_window()


class GraphWindow(CustomWindow):

    def __init__(self, master, hist, controller: customtkinter.CTk, message, *args, **kwargs):
        super().__init__(master, controller, message, *args, **kwargs)

        self.geometry(CustomWindow.center_window(
            self, 500, 500, self._get_window_scaling()))

        self.title("Gráfico del modelo de " + message)

        self.fig = Figure(figsize=(5, 5),
                          dpi=70)

        plot = self.fig.add_subplot(111)
        plot.plot(hist.history['loss'])
        plot.plot(hist.history['val_loss'])
        plot.plot(hist.history['accuracy'])
        plot.plot(hist.history['val_accuracy'])
        plot.legend(['Training Loss', 'Validation Loss',
                    'Training Accuracy', 'Validation Accuracy'], loc='center right')

        canvas = FigureCanvasTkAgg(self.fig,
                                   master=self)

        canvas.draw()

        # placing the canvas on the Tkinter window
        w = canvas.get_tk_widget()

        w.grid(padx=75, pady=30, sticky="s")

        button_accept = customtkinter.CTkButton(
            self, text="Guardar", command=self._save, font=self._button_font, width=150,
            height=50, corner_radius=20, fg_color="RoyalBlue3", hover_color="RoyalBlue4")
        button_accept.place(relx=0.3, rely=0.9, anchor=customtkinter.CENTER)

        button_accept = customtkinter.CTkButton(
            self, text="Aceptar", command=self._accept, font=self._button_font, width=150,
            height=50, corner_radius=20, fg_color="lime green", hover_color="forest green")
        button_accept.place(relx=0.7, rely=0.9, anchor=customtkinter.CENTER)

        self._block_on_window()

    def _save(self):

        directory = customtkinter.filedialog.asksaveasfilename(initialdir="./",
                                                               title="Seleccione donde guardar la gráfica",
                                                               filetypes=[('Images', '*.jpg *.jpeg *.png')])
        if len(directory) > 0:
            extension = ".png"
            if ".png" in directory:
                extension = ""
            self.fig.savefig(directory+extension)
        self.master.setvar(name="window_accept", value=False)


class LayerEditWindow(CustomWindow):
    _combo_box_font = ("Times", 16)

    def __init__(self, master, dictionary, number, controller: customtkinter.CTk, message, alias, *args, **kwargs):
        super().__init__(master, controller, message, *args, **kwargs)

        self.activations = [
            activation.value for activation in RNMNParams.RNMNActivations]
        self.params = dict()
        self.geometry(CustomWindow.center_window(
            self, 720, 400, self._get_window_scaling()))
        self.title("Edición de la capa")

        label = customtkinter.CTkLabel(
            self, text=message, font=self._title_font)
        label.place(relx=0.5, rely=0.2, anchor=customtkinter.CENTER)
        self.alias = alias
        self.number = number
        self.dictionary = dictionary
        if "params" not in self.dictionary.keys():
            self._init_vars()
        else:
            for k in self.dictionary['params'].keys():
                self.params[k] = self.dictionary['params'][k]
        self.set_widgets()

        button_accept = customtkinter.CTkButton(
            self, text="Guardar", command=self._accept, font=self._button_font, width=150,
            height=50, corner_radius=20, fg_color="RoyalBlue3", hover_color="RoyalBlue4")
        button_accept.place(relx=0.7, rely=0.9, anchor=customtkinter.CENTER)

        button_accept = customtkinter.CTkButton(
            self, text="Cancelar", command=self._cancel, font=self._button_font, width=150,
            height=50, corner_radius=20, fg_color="brown3", hover_color="brown4")
        button_accept.place(relx=0.3, rely=0.9, anchor=customtkinter.CENTER)

        self._block_on_window()

    def _cancel(self):
        self.master.setvar(name="window_accept", value=False)
        self.destroy()

    def validate(self):
        return True


    def _accept(self):
        if not self.validate():
            ErrorWindow(master=self.master, controller=self.controller,
                            message="Porfavor introduzca un valor numérico")
        else:
            self.dictionary['params'] = self.params
            return super()._accept()

    def set_widgets(self):
        pass

    def _init_vars(self):
        pass


class DenseLayerEditWindow(LayerEditWindow):

    def _add_neurons(self, value):
        self.label_units.configure(
            text="neuronas "+str(self.params["units"].get()))

    def _init_vars(self):
        self.params['units'] = customtkinter.IntVar(
            master=self.master, value=128, name="units_layer_" + str(self.number) + "_"+self.alias)

        self.params['activation'] = customtkinter.StringVar(
            master=self.master, value=self.activations[0], name="activation_layer_" + str(self.number) + "_"+self.alias)

    def set_widgets(self):
        self.label_main = customtkinter.CTkLabel(
            master=self, text="Activation", font=self._button_font)
        self.label_main.place(relx=0.7, rely=0.4, anchor=customtkinter.CENTER)

        self.activation = customtkinter.CTkComboBox(
            master=self, values=self.activations, state="readonly", variable=self.params['activation'], font=self._combo_box_font, width=100)

        self.activation.place(relx=0.7, rely=0.5, anchor=customtkinter.CENTER)

        slide = customtkinter.CTkSlider(master=self, from_=1, to=255, command=lambda value: self._add_neurons(value),
                                        variable=self.params["units"])

        slide.place(relx=0.2, rely=0.5, anchor=customtkinter.CENTER)

        self.label_units = customtkinter.CTkLabel(
            master=self, text="neuronas "+str(self.params["units"].get()), font=self._button_font)
        self.label_units.place(
            relx=0.2, rely=0.4, anchor=customtkinter.CENTER)


class EmbeddingLayerEditWindow(LayerEditWindow):

    def _init_vars(self):
        self.params['input_dim'] = customtkinter.StringVar(
            master=self.master, value="20000", name="input_dim_layer_" + str(self.number) + "_"+self.alias)

        self.params['output_dim'] = customtkinter.StringVar(
            master=self.master, value="128", name="output_dim_layer_" + str(self.number) + "_"+self.alias)
        
    def set_widgets(self):
        self.label_main = customtkinter.CTkLabel(
            master=self, text="Entradas", font=self._button_font)
        self.label_main.place(relx=0.7, rely=0.4, anchor=customtkinter.CENTER)

        self.in_dim = customtkinter.CTkEntry(master=self, textvariable=self.params['input_dim'],
            width=100)
        
        self.in_dim.place(relx=0.7, rely=0.5, anchor=customtkinter.CENTER)

        self.out_dim = customtkinter.CTkEntry(master=self, textvariable=self.params['input_dim'],
            width=100)
        

        self.out_dim.place(relx=0.2, rely=0.5, anchor=customtkinter.CENTER)

        self.label_units = customtkinter.CTkLabel(
            master=self, text="Salidas", font=self._button_font)
        self.label_units.place(
            relx=0.2, rely=0.4, anchor=customtkinter.CENTER)

    def validate(self):
        return (self.params['input_dim'].get().isnumeric() and self.params['output_dim'].get().isnumeric())

class DropoutLayerEditWindow(LayerEditWindow):

    def set_widgets(self):
        pass


class Conv1DLayerEditWindow(LayerEditWindow):

    def set_widgets(self):
        pass


class GlobalMaxPooling1DLayerEditWindow(LayerEditWindow):

    def set_widgets(self):
        pass


class Conv2DLayerEditWindow(LayerEditWindow):

    def set_widgets(self):
        pass


class MaxPooling2DLayerEditWindow(LayerEditWindow):

    def set_widgets(self):
        pass


class FlattenLayerEditWindow(LayerEditWindow):

    def set_widgets(self):
        pass
