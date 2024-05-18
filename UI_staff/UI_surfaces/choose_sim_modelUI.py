import os
from colors import Color as C
from UI_staff.UI import UI
from UI_staff.UI_Elements import MenuButton, ButtonList, Label


class ChooseSimModelUI(UI):
    def __init__(self, window_size):
        super().__init__(window_size)
        self.init_elements()
        self.draw_elements()

    def init_elements(self):
        self.init_buttons()
        self.add_button_list()
        self.add_labels()

    def init_buttons(self):
        button_dimensions = (200,50)

        offline_game_button = MenuButton("Запустить модель", 300, 100, button_dimensions=button_dimensions,
                                         action=None, color=C.yellow, font_size=24, font_name="Arial", name= "start_simulation")

        exit_button = MenuButton("Выход", 300, 500, button_dimensions=button_dimensions,
                                 action=None, color=C.yellow, font_size=24, font_name="Arial",name = "exit")


        self.add_element(0,offline_game_button)
        self.add_element(0,exit_button)

    def add_button_list(self):
        map_saves = ButtonList(position=(300,200),name= "map_saves")
        for save_name in os.listdir("./model_saves"):
            map_saves.add_element(str(save_name), save_name)
        self.add_element(0,map_saves)

    def add_labels(self):
        choose_model_label = Label("Выберите модель", position=(300,175), name= "choose_model_label")

        self.add_element(0,choose_model_label)
