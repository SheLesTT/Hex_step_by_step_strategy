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


    def find_element(self, name):
        for layer in self.elements:
            for element in layer:
                if element.name == name:
                    self.logger.debug(f"found  {element}, with name {name}")
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
            print("this is elements", self.elements[1])
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




class EditorUI(UI):
    def __init__(self, window_size, game_map,):
        super().__init__(window_size)
        self.UI_surface = None
        self.game_map = game_map
        self.init_elements()
        self.draw_elements()


    def save_game(self):
        self.game_map.save_to_json("json_save")

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


