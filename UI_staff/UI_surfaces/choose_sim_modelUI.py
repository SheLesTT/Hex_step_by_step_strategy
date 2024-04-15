import os

from UI_staff.UI import UI
from UI_staff.UI_Elements import MenuButton, ButtonList


class ChooseSimModelUI(UI):
    def __init__(self, window_size):
        super().__init__(window_size)
        self.init_elements()
        self.draw_elements()

    def init_elements(self):
        self.init_buttons()
        self.add_button_list()

    def init_buttons(self):
        button_dimensions = (200,50)

        offline_game_button = MenuButton("Start Simulation", 200, 100, button_dimensions=button_dimensions,
                                         action=None, color=(0, 0, 255), font_size=24, font_name="Arial", name= "start_simulation")

        exit_button = MenuButton("Exit", 200, 400, button_dimensions=button_dimensions,
                                 action=None, color=(0, 0, 255), font_size=24, font_name="Arial",name = "exit")


        self.add_element(0,offline_game_button)
        self.add_element(0,exit_button)

    def add_button_list(self):
        map_saves = ButtonList(position=(500,500),name= "map_saves")
        for save_name in os.listdir("./model_saves"):
            map_saves.add_element(str(save_name), save_name)
        self.add_element(0,map_saves)
