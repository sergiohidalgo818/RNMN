'''This file defines the RNMNAppGui Class'''

import tkinter
import tkinter.font
import customtkinter
from RNMNParent import RNMNParams


class SelectNetTabView(customtkinter.CTkTabview):

    _title_font = ("Times", 25, 'bold')
    _button_font = ("Times", 20, )


    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self._segmented_button.configure(font=self._button_font)
        self.add("Modelo de texto")
        self.add("Modelo de audio")
        self.add("Modelo de imagen")

        self.losses = [loss.value for loss in RNMNParams.RNMNLosses]
        self.optimizers = [
            optimizer.value for optimizer in RNMNParams.RNMNOptimizers]
        self.metrics = [metric.value for metric in RNMNParams.RNMNMetrics]

        self.add_model_image = customtkinter.BooleanVar()

        self.model_tab_create("Modelo de texto")

        self.model_tab_create("Modelo de audio")

        self.model_tab_create("Modelo de imagen")

    def model_tab_create(self, tab_name):

        add_model: customtkinter.BooleanVar
        optimizer_var: customtkinter.StringVar
        loss_var: customtkinter.StringVar
        title: str
        alias: str

        alias = tab_name.split(" ")[2]

        title = customtkinter.CTkLabel(master=self.tab(
            tab_name), text="Ajustar losses", font=self._button_font)
        title.place(relx=0.02, rely=0.1, anchor=customtkinter.W)
        loss_var = customtkinter.StringVar(
            master=self.master, value=self.losses[0], name="loss_"+alias)
        combobox_loss = customtkinter.CTkComboBox(master=self.tab(tab_name), values=self.losses,
                                                       state="readonly",
                                                       variable=loss_var, font=self._button_font, width=200)
        combobox_loss.place(relx=0.13, rely=0.1, anchor=customtkinter.W)

        title = customtkinter.CTkLabel(master=self.tab(
            tab_name), text="Ajustar optimizer", font=self._button_font)
        title.place(relx=0.4, rely=0.1, anchor=customtkinter.CENTER)
        optimizer_var = customtkinter.StringVar(
            master=self.master, value=self.optimizers[0], name="optimizer_"+alias)
        combobox_optimizer = customtkinter.CTkComboBox(master=self.tab(tab_name), values=self.optimizers,
                                                            state="readonly", 
                                                            variable=optimizer_var, font=self._button_font, width=200)
        combobox_optimizer.place(
            relx=0.565, rely=0.1, anchor=customtkinter.CENTER)

        title = customtkinter.CTkLabel(master=self.tab(
            tab_name), text="Seleccionar las métricas deseadas", font=self._button_font)
        title.place(relx=0.93, rely=0.1, anchor=customtkinter.E)


        cont = 1
        contx = 0.82
        conty = 0
        for metric in self.metrics:

            value = False
            if cont == 1:
                value = True

            check_var = customtkinter.BooleanVar(
                master=self.master, value=value, name=metric+"_"+alias)

            checbox = customtkinter.CTkCheckBox(master=self.tab(tab_name),
                                                          text=metric,
                                                          variable=check_var, onvalue=True, offvalue=False)

            checbox.place(
                relx=contx, rely=0.2+conty, anchor=customtkinter.W)

            if cont % 2 == 0:
                cont += 1
                conty += 0.1
                contx = 0.82
            else:
                cont += 1
                contx = 0.68


        add_model = customtkinter.BooleanVar(
                master=self.master, value=value, name="switch_"+alias)

        switch = customtkinter.CTkSwitch(master=self.tab(tab_name), text="Añadir modelo", 
                                 variable=add_model, onvalue=True, offvalue=False, font=self._title_font)
        
        switch.place(relx=0.5, rely=0.68, anchor=customtkinter.CENTER)
