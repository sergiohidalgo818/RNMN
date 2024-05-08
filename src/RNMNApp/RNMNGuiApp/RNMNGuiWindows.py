import customtkinter
import matplotlib as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure


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

    def _accept(self):
        self.master.setvar(name="window_accept", value=True)
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

    def _accept(self):
        self.master.setvar(name="window_accept", value=True)
        self.destroy()


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

    def _accept(self):
        self.master.setvar(name="window_accept", value=True)
        self.destroy()

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

    def __init__(self, master, dictionary, controller: customtkinter.CTk, message, *args, **kwargs):
        super().__init__(master, controller, message, *args, **kwargs)

        self.geometry(CustomWindow.center_window(
            self, 720, 400, self._get_window_scaling()))
        self.title("Edición de la capa")

        label = customtkinter.CTkLabel(
            self, text=message, font=self._title_font)
        label.place(relx=0.5, rely=0.2, anchor=customtkinter.CENTER)

        button_accept = customtkinter.CTkButton(
            self, text="Aceptar", command=self._accept, font=self._button_font, width=150,
            height=50, corner_radius=20, fg_color="lime green", hover_color="forest green")
        button_accept.place(relx=0.55, rely=0.6, anchor=customtkinter.W)

        self._block_on_window()

    def _accept(self):
        self.master.setvar(name="window_accept", value=True)
        self.destroy()
