'''This file defines the RNMNAppGui Class'''

import customtkinter
from RNMNParent import RNMNParams
from .RNMNGuiWindows import DenseLayerEditWindow, EmbeddingLayerEditWindow, DropoutLayerEditWindow
from .RNMNGuiWindows import Conv1DLayerEditWindow, GlobalMaxPooling1DLayerEditWindow, Conv2DLayerEditWindow
from .RNMNGuiWindows import MaxPooling2DLayerEditWindow, FlattenLayerEditWindow, AskLayerTypeWindow


class ValidationTabError(Exception):
    '''Raised when there is an error introducing parameters'''

    def __init__(self, message, *args):
        super(ValidationTabError, self).__init__(message, *args)
        self.message = message


class CustomTabView(customtkinter.CTkTabview):

    _title_font = ("Times", 25, 'bold')
    _button_font = ("Times", 20, )
    _combo_box_font = ("Times", 16)
    _alias = list()

    params_dict = dict()
    widget_dict = dict()
    positions_dict = dict()

    models_list = list()

    def __init__(self, master, controller,  **kwargs):
        super().__init__(master, **kwargs)
        self.controller = controller
        self.master = master
        self._segmented_button.configure(font=self._button_font)
        self.add("Modelo de texto")
        self.add("Modelo de imagen")
        self.add("Modelo de audio")

        self.model_tab_create("Modelo de texto", master)

        self.model_tab_create("Modelo de imagen", master)

        self.model_tab_create("Modelo de audio", master)

    def model_tab_create(self, tab_name, master):
        pass


class CreateNetTabView(CustomTabView):

    def __init__(self, master, **kwargs):
        self.activations = [
            activation.value for activation in RNMNParams.RNMNActivations]

        self.layers = [
            layer.value for layer in RNMNParams.RNMNLayers]
        self.windows_layers = dict()
        self.windows_layers['Dense'] = DenseLayerEditWindow
        self.windows_layers['Embedding'] = EmbeddingLayerEditWindow
        self.windows_layers['Dropout'] = DropoutLayerEditWindow
        self.windows_layers['Conv1D'] = Conv1DLayerEditWindow
        self.windows_layers['GlobalMaxPooling1D'] = GlobalMaxPooling1DLayerEditWindow
        self.windows_layers['Conv2D'] = Conv2DLayerEditWindow
        self.windows_layers['MaxPooling2D'] = MaxPooling2DLayerEditWindow
        self.windows_layers['Flatten'] = FlattenLayerEditWindow

        super().__init__(master, **kwargs)

    def _add_layer(self, alias):

        if self.params_dict[alias]['num_layers'].get() < 9:
            self.params_dict[alias]['num_layers'].set(
                self.params_dict[alias]['num_layers'].get()+1)
            if str("label_layer_" + str(self.params_dict[alias]['num_layers'].get())) in self.widget_dict[alias]['layers'].keys():
                self._recover_neuron_counter(
                    alias, self.params_dict[alias]['num_layers'].get())
            else:

                self.params_dict[alias]['layers_dict']['layer_' +
                                                       str(self.params_dict[alias]['num_layers'].get())] = dict()

                self.params_dict[alias]['layers_dict']['layer_'+str(self.params_dict[alias]['num_layers'].get())]["type"] = customtkinter.StringVar(
                    master=self.master, value=self.layers[0], name="type__layer_" + str(self.params_dict[alias]['num_layers'].get()) + "_"+alias)
                self.update_tab(alias)

    def _del_layer(self, alias):
        if self.params_dict[alias]['num_layers'].get() > 0:
            if "params" in self.params_dict[alias]['layers_dict']['layer_'+str(self.params_dict[alias]['num_layers'].get())].keys():
                del self.params_dict[alias]['layers_dict']['layer_' +
                                                           str(self.params_dict[alias]['num_layers'].get())]['params']
            self.params_dict[alias]['num_layers'].set(
                self.params_dict[alias]['num_layers'].get()-1)
            self.update_tab_forget(alias)

    def update_tab_forget(self, alias):

        self.widget_dict[alias]['layers']["label_layer_" +
                                          str(self.params_dict[alias]['num_layers'].get()+1)]['widget'].place_forget()

        self.widget_dict[alias]['layers']["edit_layer_" +
                                          str(self.params_dict[alias]['num_layers'].get()+1)]['widget'].place_forget()

        self.widget_dict[alias]['layers']["type_" +
                                          str(self.params_dict[alias]['num_layers'].get()+1)]['widget'].place_forget()

    def _recover_neuron_counter(self, alias, number):

        AskLayerTypeWindow(master=self.tab("Modelo de "+alias), controller=self.controller, type_layer=self.params_dict[alias]['layers_dict']['layer_'+str(
            number)]["type"], number=number,
            message="Introduzca el tipo de capa", alias=alias)
        type_of_layer = self.params_dict[alias]['layers_dict']['layer_'+str(
            number)]["type"].get()
        self.windows_layers[type_of_layer](master=self.tab("Modelo de "+alias), controller=self.controller,
                                           dictionary=self.params_dict[alias]['layers_dict']['layer_'+str(
                                               number)], number=number,
                                           message=type_of_layer, alias=alias)

        x, y = self.widget_dict[alias]['layers']["label_layer_" +
                                                 str(number)]['position']
        self.widget_dict[alias]['layers']["label_layer_" +
                                          str(number)]['widget'].place(x=x, y=y, anchor=customtkinter.CENTER)

        x, y = self.widget_dict[alias]['layers']["edit_layer_" +
                                                 str(number)]['position']
        self.widget_dict[alias]['layers']["edit_layer_" +
                                          str(number)]['widget'].place(x=x, y=y, anchor=customtkinter.CENTER)

        x, y = self.widget_dict[alias]['layers']["edit_layer_" +
                                                 str(number)]['position']
        self.widget_dict[alias]['layers']["edit_layer_" +
                                          str(number)]['widget'].place(x=x, y=y, anchor=customtkinter.CENTER)

        x, y = self.widget_dict[alias]['layers']["type_" +
                                                 str(number)]['position']
        self.widget_dict[alias]['layers']["type_" +
                                          str(number)]['widget'].place(x=x, y=y, anchor=customtkinter.CENTER)

    def _edit_layer_type(self, tab_name, button, number, alias, value):
        button.configure(command=lambda: self.windows_layers[value](master=self.tab(tab_name), controller=self.controller,
                                                                    dictionary=self.params_dict[alias]['layers_dict']['layer_'+str(
                                                                        number)], number=number,
                                                                    message=value, alias=alias))
        if "params" in self.params_dict[alias]['layers_dict']['layer_'+str(number)].keys():
            del self.params_dict[alias]['layers_dict']['layer_' +
                                                       str(number)]['params']

    def _create_neuron_counter(self, tab_name, number, alias, x, y):

        AskLayerTypeWindow(master=self.tab(tab_name), controller=self.controller, type_layer=self.params_dict[alias]['layers_dict']['layer_'+str(
            number)]["type"], number=number,
            message="Introduzca el tipo de capa", alias=alias)

        self.widget_dict[alias]['layers']["label_layer_" +
                                          str(number)] = dict()

        self.widget_dict[alias]['layers']["label_layer_" + str(number)]['widget'] = customtkinter.CTkLabel(master=self.tab(
            tab_name), text="Capa " + str(number) + " ", font=self._button_font)
        self.widget_dict[alias]['layers']["label_layer_" + str(number)]['widget'].place(
            x=x+40, y=y-65, anchor=customtkinter.CENTER)
        self.widget_dict[alias]['layers']["label_layer_" +
                                          str(number)]['position'] = (x+40, y-65)

        self.widget_dict[alias]['layers']["type_" + str(number)] = dict()

        self.widget_dict[alias]['layers']['edit_layer_' +
                                          str(number)] = dict()

        type_of_layer = self.params_dict[alias]['layers_dict']['layer_'+str(
            number)]["type"].get()
        self.widget_dict[alias]['layers']['edit_layer_'+str(number)]['widget'] = customtkinter.CTkButton(self.tab(
            tab_name), text="Edit layer", font=self._button_font, width=30, command=lambda: self.windows_layers[type_of_layer](master=self.tab(tab_name), controller=self.controller,
                                                                                                                               dictionary=self.params_dict[alias]['layers_dict']['layer_'+str(
                                                                                                                                   number)], number=number,
                                                                                                                               message=type_of_layer, alias=alias), height=10, corner_radius=40, fg_color="lime green", hover_color="forest green")
        self.widget_dict[alias]['layers']['edit_layer_' +
                                          str(number)]['widget'].place(x=x+130, y=y-30, anchor=customtkinter.CENTER)

        self.widget_dict[alias]['layers']["edit_layer_" +
                                          str(number)]['position'] = (x+130, y-30)
        self.widget_dict[alias]['layers']["type_" + str(number)]['widget'] = customtkinter.CTkComboBox(master=self.tab(tab_name),
                                                                                                       command=lambda value: self._edit_layer_type(
                                                                                                           tab_name, self.widget_dict[alias]['layers']['edit_layer_'+str(number)]['widget'], number, alias, value),
                                                                                                       values=self.layers, state="readonly",
                                                                                                       variable=self.params_dict[alias]['layers_dict']['layer_'+str(
                                                                                                           self.params_dict[alias]['num_layers'].get())]["type"],
                                                                                                       font=self._combo_box_font, width=200)
        self.widget_dict[alias]['layers']["type_" +
                                          str(number)]['widget'].place(x=x-30, y=y-30, anchor=customtkinter.CENTER)
        self.widget_dict[alias]['layers']["type_" +
                                          str(number)]['position'] = (x-30, y-30)

        self.windows_layers[type_of_layer](master=self.tab(tab_name), controller=self.controller,
                                           dictionary=self.params_dict[alias]['layers_dict']['layer_'+str(
                                               number)], number=number,
                                           message=type_of_layer, alias=alias)

    def update_tab(self, alias):
        self._create_neuron_counter(
            "Modelo de "+alias, self.params_dict[alias]['num_layers'].get(), alias, self.positions_dict[alias]['contx'], self.positions_dict[alias]['conty'])
        if self.positions_dict[alias]['cont'] % 3 == 0:
            self.positions_dict[alias]['cont'] += 1
            self.positions_dict[alias]['conty'] += 105
            self.positions_dict[alias]['contx'] = 145
        else:
            self.positions_dict[alias]['cont'] += 1
            self.positions_dict[alias]['contx'] += 360

    def _auto(self, alias):
        if self.params_dict[alias]['auto_in'].get():
            self.widget_dict[alias]['entry_in'].configure(
                state="disabled", fg_color="grey")
            self.widget_dict[alias]['title_in'].configure(text_color="grey")

        else:
            self.widget_dict[alias]['entry_in'].configure(
                state="normal", text_color=['gray10', '#DCE4EE'])
            self.widget_dict[alias]['title_in'].configure(
                text_color=['gray10', '#DCE4EE'])

    def model_tab_create(self, tab_name, master):

        alias = tab_name.split(" ")[2]

        self.params_dict[alias] = dict()
        self.params_dict[alias]['layers_dict'] = dict()

        self.widget_dict[alias] = dict()
        self.widget_dict[alias]['layers'] = dict()

        self.positions_dict[alias] = dict()
        self.positions_dict[alias]['cont'] = 1
        self.positions_dict[alias]['contx'] = 145
        self.positions_dict[alias]['conty'] = 180

        self._alias.append(alias)

        tab_name = tab_name

        self.widget_dict[alias]['title_in'] = customtkinter.CTkLabel(master=self.tab(
            tab_name), text="Número de entradas ", font=self._button_font)
        self.widget_dict[alias]['title_in'].place(
            relx=0.02, rely=0.1, anchor=customtkinter.W)

        self.params_dict[alias]['num_inputs'] = customtkinter.StringVar(
            master=master, value="64",  name="num_inputs_" + alias)
        self.widget_dict[alias]['entry_in'] = customtkinter.CTkEntry(master=self.tab(
            tab_name), textvariable=self.params_dict[alias]['num_inputs'],
            width=100)
        self.widget_dict[alias]['entry_in'].place(
            relx=0.18, rely=0.1, anchor=customtkinter.W)

        self.widget_dict[alias]['entry_in'].configure(
            state="disabled", text_color="grey")
        self.widget_dict[alias]['title_in'].configure(text_color="grey")

        self.params_dict[alias]['auto_in'] = customtkinter.BooleanVar(
            master=master, value=True,  name="auto_in" + alias)

        self.widget_dict[alias]['auto_in'] = customtkinter.CTkCheckBox(master=self.tab(
            tab_name), variable=self.params_dict[alias]['auto_in'], text="auto", command=lambda: self._auto(alias))
        self.widget_dict[alias]['auto_in'].place(
            relx=0.28, rely=0.1, anchor=customtkinter.W)

        self.params_dict[alias]['num_layers'] = customtkinter.IntVar(
            master=master, value=0, name="num_layers_" + alias)

        title = customtkinter.CTkLabel(master=self.tab(
            tab_name), text="Añadir capa oculta", font=self._button_font)
        title.place(relx=0.37, rely=0.1, anchor=customtkinter.W)
        add_layer = customtkinter.CTkButton(
            master=self.tab(
                tab_name), command=lambda: self._del_layer(alias), text="-", font=self._button_font, width=30,
            height=10, corner_radius=40, fg_color="brown3", hover_color="brown4")
        add_layer.place(relx=0.52, rely=0.1, anchor=customtkinter.W)
        del_layer = customtkinter.CTkButton(
            master=self.tab(
                tab_name), text="+", font=self._button_font, width=30, command=lambda: self._add_layer(alias),
            height=10, corner_radius=40, fg_color="lime green", hover_color="forest green")
        del_layer.place(relx=0.55, rely=0.1, anchor=customtkinter.W)

        title_out = customtkinter.CTkLabel(master=self.tab(
            tab_name), text="Número de salidas ", font=self._button_font)
        title_out.place(relx=0.6502, rely=0.1, anchor=customtkinter.W)

        self.params_dict[alias]['layers_dict']['layer_out'] = dict()
        self.params_dict[alias]['layers_dict']['layer_out']['params'] = dict()
        self.params_dict[alias]['layers_dict']['layer_out']['type'] = customtkinter.StringVar(
            master=master, value="Dense", name="type_outputs_" + alias)
        self.params_dict[alias]['layers_dict']['layer_out']['params']["units"] = customtkinter.StringVar(
            master=master, value="10", name="num_outputs_" + alias)

        input = customtkinter.CTkEntry(master=self.tab(
            tab_name), textvariable=self.params_dict[alias]['layers_dict']['layer_out']['params']['units'], width=100)
        input.place(relx=0.802, rely=0.1, anchor=customtkinter.W)

        self.params_dict[alias]['layers_dict']['layer_out']['params']['activation'] = customtkinter.StringVar(
            master=master, value=self.activations[2], name="activation_" + alias)

        combobox_act = customtkinter.CTkComboBox(master=self.tab(tab_name), values=self.activations,
                                                 state="readonly",
                                                 variable=self.params_dict[alias]['layers_dict'][
                                                     'layer_out']['params']['activation'],
                                                 width=100)
        combobox_act.place(relx=0.898, rely=0.1, anchor=customtkinter.W)

        self.params_dict[alias]['add_model'] = customtkinter.BooleanVar(
            master=self.master, value=False, name="switch_" + alias)

        switch = customtkinter.CTkSwitch(master=self.tab(tab_name), text="Añadir modelo",
                                         variable=self.params_dict[alias]['add_model'], onvalue=True, offvalue=False, font=self._title_font)

        switch.place(relx=0.5, rely=0.68, anchor=customtkinter.CENTER)

    def validate(self):
        for alias in self._alias:
            if not self.params_dict[alias]['num_inputs'].get().isnumeric() or not self.params_dict[alias]['layers_dict']['layer_out']['params']['units'].get().isnumeric():
                raise ValidationTabError(
                    "Error on parameters")
            elif int(self.params_dict[alias]['num_inputs'].get()) <= 0 or int(self.params_dict[alias]['layers_dict']['layer_out']['params']['units'].get()) <= 0:
                raise ValidationTabError(
                    "Error on parameters")
