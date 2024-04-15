import os
from collections import defaultdict

from Modeling.CityGraph import CityGraph
from player_actions.UI_Elements import *
from logger import  logger
pygame.font.init()
font_size = 20
font = pygame.font.SysFont("Arial", font_size)

class UI:
    def __init__(self, window_size):
        self.window_size = window_size
        self.elements = [[],[]]
        self.logger = logger.get_logger("UI")
        self.UI_surface = None

    def add_layer (self, element):
        self.elements.append([])
        self.logger.info(f"Appended level, there are total {len(element)} layers")

    def add_element(self, layer: int, element):
        try:
            self.elements[layer].append(element)
            self.logger.debug(f"added element {element}, to layer {layer}")
        except ValueError:
            print("invalid layer number")

    def __getitem__(self, name):
        return self.find_element(name)
    def find_element(self, name):
        for layer in self.elements:
            for element in layer:
                if element.name == name:
                    # self.logger.debug(f"found  {element}, with name {name}")
                    return element

    def open_element(self, name):
        self.find_element(name).make_visible()
        self.draw_elements()
        self.logger.debug(f"made element with name {name} visible ")

    def hide_element(self, name):
        self.find_element(name).hide()
        self.draw_elements()
        self.logger.debug(f"made element with name {name} invisible ")

    def hide_layer_elements(self, layer):
        if not isinstance(layer, list):
            layer = [layer]
        for lvl in layer:
            for element in self.elements[lvl]:
                element.hide()
        self.draw_elements()
        self.logger.debug(f"hide UI element of layer {layer} ")

    def draw_elements(self):
        self.UI_surface = pygame.Surface(self.window_size, pygame.SRCALPHA)
        for layer in self.elements:
            for element in layer:
                if element.visible:
                    element.draw(self.UI_surface)

    def check_click(self, mouse_pos: tuple[int, int]) -> bool:
        for layer in reversed(self.elements):
            for element in layer:
                if element.visible and element.check_click(mouse_pos):
                    self.logger.info(f"UI element {element}, was clicked")
                    return True
        return False

    def check_scroll(self, scroll: int) -> bool:
        for layer in reversed(self.elements):
            for element in layer:
                if element.visible and isinstance(element, Scrollable):
                    element.check_scroll(scroll)
                    element.draw(self.UI_surface)
                    self.logger.info(f"UI element {element}, was scrolled")
                    return True

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

class EditorUI(UI):
    def __init__(self, window_size, game_map,):
        super().__init__(window_size)
        self.UI_surface = None
        self.game_map = game_map
        self.init_elements()
        self.draw_elements()


    def save_game(self):
        self.game_map.save_to_json()

    def init_elements(self):
        self.add_buttons()
        self.add_hexes_list()
        self.add_editor_mods_list()
        self.add_surface()


    def add_surface(self):
        surface = UiSurface(size=(300, 800), position=(500, 0), visible=False, name ="city_surface" )
        self.add_element(1,surface)


    def add_hexes_list(self):
        button_list = ButtonList(position=(200, 0), name="hex_types")
        hexes_types = ["HexagonLand", "HexagonMountain", "HexagonSea", "HexagonEmpty"]
        [button_list.add_element(hex_type, hex_type) for hex_type in hexes_types]
        self.add_element(0,button_list)

    def add_editor_mods_list(self):
        button_list = ButtonList(position=(0, 0), name="editor_mods")
        modes = ["Hexes", "Rivers", "Roads", "Buildings", "None"]
        [button_list.add_element(mode, mode) for mode in modes]
        self.add_element(0,button_list)

    def add_buttons(self, ):

        display_size = pygame.display.get_surface().get_size()
        button_size = (100, 100)
        undo_button = MenuButton("Undo", 700, 700, button_size,name="undo")
        delete_button = MenuButton("Delete", 600,600,button_size, name="delete")
        finish_move = MenuButton("Create graph", display_size[0] - 100, display_size[1] - 100 - 100 * 3,
                                 button_dimensions=button_size, action=self.game_map.create_graph, color=(255, 0, 0),
                                 font_size=24, font_name="Arial")

        load_to_json = MenuButton("Save Game", display_size[0] - 100, display_size[1] - 100 - 100 * 4,
                                  button_dimensions=button_size, action=self.save_game, color=(255, 0, 0),
                                  font_size=24, font_name="Arial")

        exit_button = MenuButton("Exit", 700,0,button_size, name="exit")
        self.add_element(0, undo_button)
        self.add_element(0, finish_move)
        self.add_element(0, load_to_json)
        self.add_element(0, delete_button)
        self.add_element(0, exit_button)

    def subscribe_text_elements(self, observer, ):
        for layer in self.elements:
            for element in layer:
                if isinstance(element, TextObservable):
                    element.add_observer(observer)

class SimUI(UI):
    def __init__(self, window_size, game_map,):
        super().__init__(window_size)
        self.window_size = window_size
        self.game_map = game_map

        self.init_elements()
        self.draw_elements()

    def start_simulation(self):
        graph = CityGraph(self.game_map)
        graph.run_simulation()
        # print("mulation")
    def init_elements(self):
        self.add_buttons()
        self.add_surface()

    def add_buttons(self,):

        display_size = pygame.display.get_surface().get_size()
        button_size = (100, 100)

        start_simlation= MenuButton("mulation", display_size[0]-100, display_size[1]-100-100*4,
                                    button_dimensions=button_size, action=self.start_simulation, color=(255, 0, 0),
                                    font_size=24, font_name="Arial")

        self.add_element(0,start_simlation)

    def add_surface(self):
        print("Calling add surface")
        surface = UiSurface(size=(300,800), position=(500,0),visible=False)
        surface.name = "city_surface"
        self.add_element(1,surface)


