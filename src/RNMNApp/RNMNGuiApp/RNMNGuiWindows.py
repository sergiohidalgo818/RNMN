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
        self.protocol('WM_DELETE_WINDOW', self._cancel)

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

    def _cancel(self):
        self.master.setvar(name="window_accept", value=False)
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
        for key in hist.history.keys():
            plot.plot(hist.history[key])

        plot.legend(hist.history.keys(), loc='center right')

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


class AskLayerTypeWindow(CustomWindow):
    _combo_box_font = ("Times", 20)
    _title_font = ("Times", 25, 'bold')

    def __init__(self, master, type_layer, number, controller: customtkinter.CTk, message, alias, *args, **kwargs):
        super().__init__(master, controller, message, *args, **kwargs)
        self.layers = [
            layer.value for layer in RNMNParams.RNMNLayers]
        self.geometry(CustomWindow.center_window(
            self, 400, 300, self._get_window_scaling()))
        self.title("Tipo de capa")

        label = customtkinter.CTkLabel(
            self, text=message, font=self._title_font)
        label.place(relx=0.5, rely=0.1, anchor=customtkinter.CENTER)

        button_accept = customtkinter.CTkButton(
            self, text="Aceptar", command=self._accept, font=self._button_font, width=150,
            height=50, corner_radius=20, fg_color="RoyalBlue3", hover_color="RoyalBlue4")
        button_accept.place(relx=0.5, rely=0.9, anchor=customtkinter.CENTER)

        type_layer = customtkinter.StringVar(
            master=self.master, value=self.layers[0], name="type__layer_" + str(number) + "_"+alias)

        self.activation = customtkinter.CTkComboBox(
            master=self, values=self.layers, state="readonly", variable=type_layer, font=self._combo_box_font, width=220)

        self.activation.place(relx=0.5, rely=0.5, anchor=customtkinter.CENTER)
        self._block_on_window()


class LayerEditWindow(CustomWindow):
    _combo_box_font = ("Times", 16)
    _title_font = ("Times", 25, 'bold')

    def __init__(self, master, dictionary, number, controller: customtkinter.CTk, message, alias, *args, **kwargs):
        super().__init__(master, controller, message, *args, **kwargs)

        self.activations = [
            activation.value for activation in RNMNParams.RNMNActivations]
        self.paddings = [
            padding.value for padding in RNMNParams.RNMNPaddings]
        self.params = dict()
        self.geometry(CustomWindow.center_window(
            self, 580, 400, self._get_window_scaling()))
        self.title("Edición de la capa")

        label = customtkinter.CTkLabel(
            self, text=message, font=self._title_font)
        label.place(relx=0.5, rely=0.1, anchor=customtkinter.CENTER)
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
        button_accept.place(relx=0.8, rely=0.9, anchor=customtkinter.CENTER)

        button_accept = customtkinter.CTkButton(
            self, text="Cancelar", command=self._cancel, font=self._button_font, width=150,
            height=50, corner_radius=20, fg_color="brown3", hover_color="brown4")
        button_accept.place(relx=0.2, rely=0.9, anchor=customtkinter.CENTER)

        self._block_on_window()

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
            text="Neuronas "+str(self.params["units"].get()))

    def _init_vars(self):
        self.params['units'] = customtkinter.IntVar(
            master=self.master, value=128, name="units_layer_" + str(self.number) + "_"+self.alias)

        self.params['activation'] = customtkinter.StringVar(
            master=self.master, value=self.activations[0], name="activation_layer_" + str(self.number) + "_"+self.alias)

    def set_widgets(self):
        self.label_main = customtkinter.CTkLabel(
            master=self, text="Activación", font=self._button_font)
        self.label_main.place(relx=0.7, rely=0.4, anchor=customtkinter.CENTER)

        self.activation = customtkinter.CTkComboBox(
            master=self, values=self.activations, state="readonly", variable=self.params['activation'], font=self._combo_box_font, width=100)

        self.activation.place(relx=0.7, rely=0.5, anchor=customtkinter.CENTER)

        slide = customtkinter.CTkSlider(master=self, from_=1, to=255, command=lambda value: self._add_neurons(value),
                                        variable=self.params["units"])

        slide.place(relx=0.3, rely=0.5, anchor=customtkinter.CENTER)

        self.label_units = customtkinter.CTkLabel(
            master=self, text="Neuronas "+str(self.params["units"].get()), font=self._button_font)
        self.label_units.place(
            relx=0.3, rely=0.4, anchor=customtkinter.CENTER)


class EmbeddingLayerEditWindow(LayerEditWindow):

    def _init_vars(self):
        self.params['input_dim'] = customtkinter.StringVar(
            master=self.master, value="20000", name="input_dim_layer_" + str(self.number) + "_"+self.alias)

        self.params['output_dim'] = customtkinter.StringVar(
            master=self.master, value="128", name="output_dim_layer_" + str(self.number) + "_"+self.alias)

    def set_widgets(self):
        self.label_main = customtkinter.CTkLabel(
            master=self, text="Entradas", font=self._button_font)
        self.label_main.place(relx=0.3, rely=0.4, anchor=customtkinter.CENTER)

        self.in_dim = customtkinter.CTkEntry(master=self, textvariable=self.params['input_dim'],
                                             width=100)

        self.in_dim.place(relx=0.3, rely=0.5, anchor=customtkinter.CENTER)

        self.out_dim = customtkinter.CTkEntry(master=self, textvariable=self.params['output_dim'],
                                              width=100)

        self.out_dim.place(relx=0.7, rely=0.5, anchor=customtkinter.CENTER)

        self.label_units = customtkinter.CTkLabel(
            master=self, text="Salidas", font=self._button_font)
        self.label_units.place(
            relx=0.7, rely=0.4, anchor=customtkinter.CENTER)

    def validate(self):
        return (self.params['input_dim'].get().isnumeric() and self.params['output_dim'].get().isnumeric())


class DropoutLayerEditWindow(LayerEditWindow):

    def _init_vars(self):
        self.params['rate'] = customtkinter.StringVar(
            master=self.master, value="0.5", name="rate_layer_" + str(self.number) + "_"+self.alias)

    def set_widgets(self):
        self.label_main = customtkinter.CTkLabel(
            master=self, text="Ratio", font=self._button_font)
        self.label_main.place(relx=0.5, rely=0.4, anchor=customtkinter.CENTER)

        self.in_dim = customtkinter.CTkEntry(master=self, textvariable=self.params['rate'],
                                             width=100)

        self.in_dim.place(relx=0.5, rely=0.5, anchor=customtkinter.CENTER)

    def validate(self):
        try:
            float(self.params['rate'].get())
        except ValueError:
            return False
        else:
            return (float(self.params['rate'].get()) <= 1) and (float(self.params['rate'].get()) > 0)


class Conv1DLayerEditWindow(LayerEditWindow):

    def _init_vars(self):
        self.params['filters'] = customtkinter.StringVar(
            master=self.master, value="128", name="filters_layer_" + str(self.number) + "_"+self.alias)

        self.params['kernel_size'] = customtkinter.StringVar(
            master=self.master, value="7", name="kernel_size_dim_layer_" + str(self.number) + "_"+self.alias)

        self.params['strides'] = customtkinter.StringVar(
            master=self.master, value="3", name="strides_dim_layer_" + str(self.number) + "_"+self.alias)

        self.params['padding'] = customtkinter.StringVar(
            master=self.master, value=self.paddings[0], name="padding_dim_layer_" + str(self.number) + "_"+self.alias)

        self.params['activation'] = customtkinter.StringVar(
            master=self.master, value=self.activations[0], name="activation_dim_layer_" + str(self.number) + "_"+self.alias)

    def set_widgets(self):
        label = customtkinter.CTkLabel(
            master=self, text="Filtros", font=self._button_font)
        label.place(relx=0.3, rely=0.2, anchor=customtkinter.CENTER)

        entry = customtkinter.CTkEntry(master=self, textvariable=self.params['filters'],
                                       width=100)
        entry.place(relx=0.3, rely=0.3, anchor=customtkinter.CENTER)

        label = customtkinter.CTkLabel(
            master=self, text="Strides", font=self._button_font)
        label.place(
            relx=0.3, rely=0.6, anchor=customtkinter.CENTER)

        entry = customtkinter.CTkEntry(master=self, textvariable=self.params['strides'],
                                       width=100)
        entry.place(relx=0.3, rely=0.7, anchor=customtkinter.CENTER)

        label = customtkinter.CTkLabel(
            master=self, text="Tamaño del kernel", font=self._button_font)
        label.place(relx=0.5, rely=0.45, anchor=customtkinter.CENTER)

        entry = customtkinter.CTkEntry(master=self, textvariable=self.params['kernel_size'],
                                       width=100)
        entry.place(relx=0.5, rely=0.55, anchor=customtkinter.CENTER)

        label = customtkinter.CTkLabel(
            master=self, text="Activación", font=self._button_font)
        label.place(relx=0.7, rely=0.2, anchor=customtkinter.CENTER)

        entry = customtkinter.CTkComboBox(
            master=self, values=self.activations, state="readonly", variable=self.params['activation'], font=self._combo_box_font, width=100)

        entry.place(relx=0.7, rely=0.3, anchor=customtkinter.CENTER)

        label = customtkinter.CTkLabel(
            master=self, text="Padding", font=self._button_font)
        label.place(relx=0.7, rely=0.6, anchor=customtkinter.CENTER)

        entry = customtkinter.CTkComboBox(
            master=self, values=self.paddings, state="readonly", variable=self.params['padding'], font=self._combo_box_font, width=100)

        entry.place(relx=0.7, rely=0.7, anchor=customtkinter.CENTER)

    def validate(self):
        return (self.params['filters'].get().isnumeric() and self.params['strides'].get().isnumeric() and self.params['kernel_size'].get().isnumeric())


class GlobalMaxPooling1DLayerEditWindow(LayerEditWindow):
    def _init_vars(self):
        self.params['keepdims'] = customtkinter.BooleanVar(
            master=self.master, value=False, name="keepdims_layer_" + str(self.number) + "_"+self.alias)

    def set_widgets(self):

        entry = customtkinter.CTkCheckBox(master=self, variable=self.params['keepdims'],
                                          width=100, text="Mantener dimensión")
        entry.place(relx=0.5, rely=0.5, anchor=customtkinter.CENTER)


class Conv2DLayerEditWindow(LayerEditWindow):
    def _init_vars(self):
        self.params['filters'] = customtkinter.StringVar(
            master=self.master, value="32", name="filters_layer_" + str(self.number) + "_"+self.alias)

        self.params['kernel_size'] = customtkinter.StringVar(
            master=self.master, value="5", name="kernel_size_dim_layer_" + str(self.number) + "_"+self.alias)

        self.params['padding'] = customtkinter.StringVar(
            master=self.master, value=self.paddings[1], name="padding_dim_layer_" + str(self.number) + "_"+self.alias)

        self.params['activation'] = customtkinter.StringVar(
            master=self.master, value=self.activations[0], name="activation_dim_layer_" + str(self.number) + "_"+self.alias)

    def set_widgets(self):
        label = customtkinter.CTkLabel(
            master=self, text="Filtros", font=self._button_font)
        label.place(relx=0.3, rely=0.2, anchor=customtkinter.CENTER)

        entry = customtkinter.CTkEntry(master=self, textvariable=self.params['filters'],
                                       width=100)
        entry.place(relx=0.3, rely=0.3, anchor=customtkinter.CENTER)

        label = customtkinter.CTkLabel(
            master=self, text="Tamaño del kernel", font=self._button_font)
        label.place(
            relx=0.3, rely=0.6, anchor=customtkinter.CENTER)

        entry = customtkinter.CTkEntry(master=self, textvariable=self.params['kernel_size'],
                                       width=100)
        entry.place(relx=0.3, rely=0.7, anchor=customtkinter.CENTER)

        label = customtkinter.CTkLabel(
            master=self, text="Activación", font=self._button_font)
        label.place(relx=0.7, rely=0.2, anchor=customtkinter.CENTER)

        entry = customtkinter.CTkComboBox(
            master=self, values=self.activations, state="readonly", variable=self.params['activation'], font=self._combo_box_font, width=100)

        entry.place(relx=0.7, rely=0.3, anchor=customtkinter.CENTER)

        label = customtkinter.CTkLabel(
            master=self, text="Padding", font=self._button_font)
        label.place(relx=0.7, rely=0.6, anchor=customtkinter.CENTER)

        entry = customtkinter.CTkComboBox(
            master=self, values=self.paddings, state="readonly", variable=self.params['padding'], font=self._combo_box_font, width=100)

        entry.place(relx=0.7, rely=0.7, anchor=customtkinter.CENTER)

    def validate(self):
        return (self.params['filters'].get().isnumeric() and self.params['kernel_size'].get().isnumeric())


class MaxPooling2DLayerEditWindow(LayerEditWindow):
    def _init_vars(self):

        self.params['padding'] = customtkinter.StringVar(
            master=self.master, value=self.paddings[1], name="padding_dim_layer_" + str(self.number) + "_"+self.alias)

    def set_widgets(self):
        label = customtkinter.CTkLabel(
            master=self, text="Padding", font=self._button_font)
        label.place(relx=0.5, rely=0.45, anchor=customtkinter.CENTER)

        entry = customtkinter.CTkComboBox(
            master=self, values=self.paddings, state="readonly", variable=self.params['padding'], font=self._combo_box_font, width=100)

        entry.place(relx=0.5, rely=0.55, anchor=customtkinter.CENTER)


class FlattenLayerEditWindow(LayerEditWindow):

    def set_widgets(self):
        label = customtkinter.CTkLabel(
            master=self, text="Flatten", font=self._button_font)
        label.place(relx=0.5, rely=0.5, anchor=customtkinter.CENTER)
