import customtkinter
import os

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
        self.transient(self.master)  # set to be on top of the main window
        self.grab_set()  # hijack all commands from the master (clicks on the main window are ignored)
        self.focus_force()
        # pause anything on the main window until this one closes
        self.master.wait_window(self)


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