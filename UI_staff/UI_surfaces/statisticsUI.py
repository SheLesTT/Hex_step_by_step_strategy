import json
import os
from colors import Color as C
from UI_staff.UI import UI
from UI_staff.UI_Elements import MenuButton, ButtonList, Label
from StatsGraphBuilder import StatsGraphBuilder


class StatisticsUI(UI):
    def __init__(self, window_size):
        super().__init__(window_size)
        self.graph_builder = StatsGraphBuilder()
        self.init_elements()
        self.draw_elements()

    def init_elements(self):
        with open("statistics.json", "r") as f:
            statistics = json.load(f)
        building = list(statistics.keys() )
        parameters = statistics[building[0]].keys()
        self.init_buttons()
        self.add_buildings_list(building)
        self.add_parameters_list(parameters)
        self.add_labels()

    def init_buttons(self):
        button_dimensions = (200,50)


        exit_button = MenuButton("Exit", 600, 0, button_dimensions=button_dimensions,
                                 action=None, color=C.yellow, font_size=24, font_name="Arial",name = "exit")


        self.add_element(0,exit_button)
    def add_labels(self):

        self.add_element(0, Label(str("Выберите населенный пункт"), (0, 0), "choose_building", C.brown))
        self.add_element(0, Label(str("Выберите параметр"), (0, 225), "choose_building", C.brown))

    def add_buildings_list(self, buildings_names):
        map_saves = ButtonList(position=(1,25),name= "buildings")
        for save_name in buildings_names:
            map_saves.add_element(str(save_name), save_name)
        [element.add_action(self.create_chart, action_args=()) for element in map_saves.elements]
        self.add_element(0,map_saves)

    def add_parameters_list(self, parameters_names):
        map_saves = ButtonList(position=(0,250),name= "parameters")
        for save_name in parameters_names:
            map_saves.add_element(str(save_name), save_name)
        [element.add_action(self.create_chart, action_args=()) for element in map_saves.elements]
        self.add_element(0,map_saves)

    def create_chart(self):
        building = self.find_element("buildings").selected_element
        parameter = self.find_element("parameters").selected_element
        graph_image =self.graph_builder.build_matplotlib_graph(building, parameter)
        self.UI_surface.blit(graph_image, (200,100))

