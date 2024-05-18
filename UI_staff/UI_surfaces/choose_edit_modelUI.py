import os
from colors import Color as C

from UI_staff.UI_Elements import MenuButton, ButtonList, TextInput, TextObservable, Label
from UI_staff.UI import UI


class ChooseSavedModelUI(UI):
    def __init__(self, window_size):
        super().__init__(window_size)
        self.init_elements()
        self.draw_elements()

    def init_elements(self):
        self.init_buttons()
        self.add_button_list()
        self.add_text_input()
        self.add_labels()

    def init_buttons(self):
        button_dimensions = (200,50)

        offline_game_button = MenuButton("Создать карту", 100, 100, button_dimensions=button_dimensions,
                                         action=None, color=C.yellow, font_size=24, font_name="Arial", name= "start_simulation")

        exit_button = MenuButton("Выход", 300, 500, button_dimensions=button_dimensions,
                                 action=None, color=C.yellow, font_size=24, font_name="Arial",name = "exit")

        map_editor_button = MenuButton("Загрузить карту", 500, 100, button_dimensions=button_dimensions,
                                       action=None, color=C.yellow , font_size=24, font_name="Arial", name = "load_map")

        self.add_element(0,offline_game_button)
        self.add_element(0,exit_button)
        self.add_element(0,map_editor_button)

    def add_button_list(self):
        map_saves = ButtonList(position=(500, 200),name= "map_saves")
        for save_name in os.listdir("./model_saves"):
            # print("name from a folder", save_name)
            map_saves.add_element(str(save_name), save_name)
        self.add_element(0,map_saves)

    def refresh_button_list(self):
        map_saves = self.find_element("map_saves")

        for save_name in os.listdir("./model_saves"):
            if save_name not in map_saves.elements.values():
                map_saves.add_element(str(save_name), save_name)
        self.draw_elements()


    def add_text_input(self):
        input_model_name = TextInput("", position=(100,200), name= "input_model_name")
        self.add_element(0,input_model_name)
        input_rows_amount = TextInput("", position=(100,300), name= "input_rows")
        self.add_element(0,input_rows_amount)
        input_columns_amount= TextInput("", position=(100,400), name= "input_columns")
        self.add_element(0,input_columns_amount)

    def add_labels(self):
        enter_name_label = Label("Введите название модели", position=(100,175), name= "enter_name_label")
        enter_map_width_label = Label("Введите ширину карты", position=(100,275), name= "enter_map_width_label")
        enter_map_height_label = Label("Введите высоту карты", position=(100,375), name= "enter_map_height_label")
        choose_map_label = Label("Выберите карту", position=(500,175), name= "choose_map_label")

        self.add_element(0,enter_name_label)
        self.add_element(0,enter_map_width_label)
        self.add_element(0,enter_map_height_label)
        self.add_element(0,choose_map_label)


    def subscribe_text_elements(self, observer, ):
        for layer in self.elements:
            for element in layer:
                if isinstance(element, TextObservable):
                    element.add_observer(observer)
