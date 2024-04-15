import os

from UI_staff.UI_Elements import MenuButton, ButtonList, TextInput, TextObservable
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

    def init_buttons(self):
        button_dimensions = (200,50)

        offline_game_button = MenuButton("Start Simulation", 200, 100, button_dimensions=button_dimensions,
                                         action=None, color=(0, 0, 255), font_size=24, font_name="Arial", name= "start_simulation")

        exit_button = MenuButton("Exit", 200, 400, button_dimensions=button_dimensions,
                                 action=None, color=(0, 0, 255), font_size=24, font_name="Arial",name = "exit")

        map_editor_button = MenuButton("Load map", 600, 100, button_dimensions=button_dimensions,
                                       action=None, color=(0, 0, 255), font_size=24, font_name="Arial", name = "load_map")

        self.add_element(0,offline_game_button)
        self.add_element(0,exit_button)
        self.add_element(0,map_editor_button)

    def add_button_list(self):
        map_saves = ButtonList(position=(500,500),name= "map_saves")
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
        input_model_name = TextInput("", position=(10,10), name= "input_model_name")
        self.add_element(0,input_model_name)
        input_rows_amount = TextInput("", position=(10,110), name= "input_rows")
        self.add_element(0,input_rows_amount)
        input_columns_amount= TextInput("", position=(10,210), name= "input_columns")
        self.add_element(0,input_columns_amount)

    def subscribe_text_elements(self, observer, ):
        for layer in self.elements:
            for element in layer:
                if isinstance(element, TextObservable):
                    element.add_observer(observer)
