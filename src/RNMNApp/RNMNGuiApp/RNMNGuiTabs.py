'''This file defines the RNMNAppGui Class'''

import tkinter
import tkinter.font
import customtkinter
from RNMNParent import RNMNParams
import json

class ValidationTabError(Exception):
    '''Raised when there is an error introducing parameters'''
    def __init__(self, message, *args):
        super(ValidationTabError, self).__init__(message, *args) 
        self.message = message  


class CreateNetTabView(customtkinter.CTkTabview):


    _title_font = ("Times", 25, 'bold')
    _button_font = ("Times", 20, )
    _alias = list()

    params_dict = dict()
    cont = 1
    contx = 0.23
    conty = 0.26

    models_list = list()

    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.master = master
        self._segmented_button.configure(font=self._button_font)

        self.add("Modelo de texto")
        self.add("Modelo de audio")
        self.add("Modelo de imagen")

        num_inputs_text = customtkinter.StringVar(
            master=self.master,  name="num_inputs_texto", value="64")
        num_inputs_text.set("64")     

        num_inputs_audio = customtkinter.StringVar(
            master=self.master,  name="num_inputs_audio", value="64")
        num_inputs_audio.set("64")     

        num_inputs_image = customtkinter.StringVar(
            master=self.master,  name="num_inputs_imagen", value="64")
        num_inputs_image.set("64")     


        self.model_tab_create("Modelo de texto", master)

        self.model_tab_create("Modelo de audio", master)

        self.model_tab_create("Modelo de imagen", master)



    def _add_neurons(self, alias, number):

        num_neurons = customtkinter.IntVar(
                master=self.master, value=1, name="layer_" + str(number) + "_"+alias)
        if num_neurons.get() < 30:
            num_neurons.set(num_neurons.get()+1)


    def _del_neurons(self, alias, number):
        num_neurons = customtkinter.IntVar(
                master=self.master, value=1, name="layer_" + str(number) + "_"+alias)
        if num_neurons.get() > 1:
            num_neurons.set(num_neurons.get()-1)

    def _add_layer(self, alias):

        num_layer = customtkinter.IntVar(
            master=self.master, name="num_layers_" + alias)
        if num_layer.get() < 5:
            num_layer.set(num_layer.get()+1)
            num_neurons = customtkinter.IntVar(
                master=self.master, value=1, name="layer_" + str(num_layer.get()) + "_"+alias)
            self.update_tab(alias)

    def _del_layer(self, alias):
        num_layer = customtkinter.IntVar(
            master=self.master,  name="num_layers_" + alias)
        if num_layer.get() > 1:
            num_layer.set(num_layer.get()-1)
            self.update_tab_forget(alias)

    def update_tab_forget(self, alias):

        num_layer = customtkinter.IntVar(
            master=self.master,  name="num_layers_" + alias)
        
        layer_forget = num_layer.get() -1


    def _create_neuron_counter (self, tab_name, number, alias, relx,rely):
        title = customtkinter.CTkLabel(master=self.tab(
            tab_name), text="Añadir neuronas a la capa " +str(number)+ " ", font=self._button_font)
        title.place(relx=relx, rely=rely, anchor=customtkinter.CENTER)

        add_layer = customtkinter.CTkButton(
            master=self.tab(
                tab_name), command=lambda: self._add_neurons(alias, number), text="-", font=self._button_font, width=30,
            height=10, corner_radius=40, fg_color="brown3", hover_color="brown4")
        add_layer.place(relx=relx+0.12, rely=rely, anchor=customtkinter.CENTER)

        del_layer = customtkinter.CTkButton(
            master=self.tab(
                tab_name), text="+", font=self._button_font, width=30, command=lambda: self._del_neurons(alias),
            height=10, corner_radius=40, fg_color="brown3", hover_color="brown4")
        del_layer.place(relx=relx+0.15, rely=rely, anchor=customtkinter.CENTER)

        num_neurons = customtkinter.IntVar(
                master=self.master, value=1, name="layer_" + str(number) + "_"+alias)
        
        title_num = customtkinter.CTkLabel(master=self.tab(
            tab_name), text="Neuronas "+ str(num_neurons.get())+ " ", )
        title_num.place(relx=relx+0.2, rely=rely, anchor=customtkinter.CENTER)

    def update_tab(self, alias):

        num_layer = customtkinter.IntVar(
                master=self.master,  name="num_layers_" + alias)

        self._create_neuron_counter ("Modelo de "+alias , num_layer.get(), alias, self.contx,self.conty)
        if self.cont % 2 == 0:
            self.cont += 1
            self.conty += 0.1
            self.contx = 0.23
        else:
            self.cont += 1
            self.contx = 0.7


    def model_tab_create(self, tab_name, master):

        add_model: customtkinter.BooleanVar

        alias = tab_name.split(" ")[2]

        self._alias.append(alias)

        tab_name = tab_name

        title_in = customtkinter.CTkLabel(master=self.tab(
            tab_name), text="Número de entradas ", font=self._button_font)
        title_in.place(relx=0.02, rely=0.1, anchor=customtkinter.W)

        num_inputs = customtkinter.StringVar(
            master=master,  name="num_inputs_" + alias)
        input = customtkinter.CTkEntry(master=self.tab(
            tab_name), textvariable=num_inputs)
        input.place(relx=0.18, rely=0.1, anchor=customtkinter.W)


        num_layer = customtkinter.IntVar(
            master=master, value=1, name="num_layers_" + alias)
        num_layer.set(1)
        title = customtkinter.CTkLabel(master=self.tab(
            tab_name), text="Añadir capa ", font=self._button_font)
        title.place(relx=0.02, rely=0.2, anchor=customtkinter.W)

        add_layer = customtkinter.CTkButton(
            master=self.tab(
                tab_name), command=lambda: self._del_layer(alias), text="-", font=self._button_font, width=30,
            height=10, corner_radius=40, fg_color="brown3", hover_color="brown4")
        add_layer.place(relx=0.13, rely=0.2, anchor=customtkinter.W)

        del_layer = customtkinter.CTkButton(
            master=self.tab(
                tab_name), text="+", font=self._button_font, width=30, command=lambda: self._add_layer(alias),
            height=10, corner_radius=40, fg_color="brown3", hover_color="brown4")
        del_layer.place(relx=0.16, rely=0.2, anchor=customtkinter.W)

  

        add_model = customtkinter.BooleanVar(
            master=self.master, value=False, name="switch_" + alias)

        switch = customtkinter.CTkSwitch(master=self.tab(tab_name), text="Añadir modelo",
                                         variable=add_model, onvalue=True, offvalue=False, font=self._title_font)

        switch.place(relx=0.5, rely=0.68, anchor=customtkinter.CENTER)


    def validate(self):
        for alias in self._alias:
            num_inputs = customtkinter.StringVar(master=self.master,  name="num_inputs_" + alias)
            if not num_inputs.get().isnumeric():
                raise ValidationTabError("Introduzca un valor numérico para el número de entradas, porfavor")

class ModifyHPNetTabView(customtkinter.CTkTabview):

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

        self.model_tab_create("Modelo de texto")

        self.model_tab_create("Modelo de audio")

        self.model_tab_create("Modelo de imagen")

    def model_tab_create(self, tab_name):

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
