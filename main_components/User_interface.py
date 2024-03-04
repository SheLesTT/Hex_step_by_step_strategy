from collections import defaultdict

import pygame

from player_actions.UI_Elements import *

pygame.font.init()
font_size = 20
font = pygame.font.SysFont("Arial", font_size)


class UI:
    def __init__(self, window_size, game_map, spawner):
        self.window_size = window_size
        self.UI_surface = None
        self.game_map = game_map
        self.spawner = spawner
        self.elements = defaultdict(list)
        self.lvl_1_elements = []
        self.lvl_2_elements = []
        self.button_lists = {}
        self.init_elements()
        self.draw_elements()

    # draw_text(self,  font =font, color= (50,50,50), x=100, y=100):
    #        text_surface = font.render(self.text, True, color)
    #        self.UI_surface.blit(text_surface, (x, y))

    def init_elements_storage(self):
        elements = defaultdict(list)
        elements[0] = []
        elements[1] = []
        return elements

    def add_layer (self, element):
       next_layer = list( self.elements.keys())[-1]
       next_layer += 1
       self.elements[next_layer] = []

    def add_element(self, layer: int, element):
        try:
            self.elements[layer].append(element)
        except ValueError:
            print("invalid layer number")


    def find_element(self, name):
        for layer in self.elements:
            for element in self.elements[layer]:
                if element.name == name:
                    return element

    def open_element(self, name):
        self.find_element(name).make_visible()
        self.draw_elements()

    def hide_element(self, name):
        self.find_element(name).hide()
        self.draw_elements()

    def hide_lvl_2_elements(self):
        for element in self.lvl_2_elements:
            element.hide()
        self.draw_elements()

    def end_turn(self, ):
        pass

    def save_game(self):
        self.game_map.save_to_json("json_save")

    def init_elements(self):
        self.add_buttons()
        self.add_hexes_list()
        self.add_editor_mods_list()
        self.add_surface()

    def draw_elements(self):
        self.UI_surface = pygame.Surface(self.window_size, pygame.SRCALPHA)
        for layer in self.elements.values():
            for element in layer:
                if element.visible:
                    element.draw(self.UI_surface)

    def add_surface(self):
        print("Calling add surface")
        surface = UiSurface(size=(300, 800), position=(500, 0), visible=False)
        surface.name = "city_surface"
        self.elements[1].append(surface)

    def add_text(self):
        text_input = TextInput()
        self.lvl_2_elements.append(text_input)
        self.text_input = text_input

    def add_hexes_list(self):
        button_list = ButtonList(position=(200, 0))
        hexes_types = ["Hexagon_land", "Hexagon_mountain", "HexagonSea", "HexagonEmpty"]
        [button_list.add_element(hex_type, hex_type) for hex_type in hexes_types]
        self.elements[0].append(button_list)
        self.button_lists["hex_types"] = button_list

    def add_editor_mods_list(self):
        button_list = ButtonList(position=(0, 0))
        modes = ["Hexes", "Rivers", "Roads", "Buildings", "None"]
        [button_list.add_element(mode, mode) for mode in modes]
        self.elements[0].append(button_list)
        self.button_lists["editor_mods"] = button_list

    def add_buttons(self, ):

        titles = ["Triangular", "Square", "Circle"]
        display_size = pygame.display.get_surface().get_size()
        button_size = (100, 100)
        for i in range(len(titles)):
            button = MenuButton(titles[i], display_size[0] - 100, display_size[1] - 100 - 100 * i, button_size,
                                action=self.hide_element, )
            self.elements[0].append(button)
        finish_move = MenuButton("Create graph", display_size[0] - 100, display_size[1] - 100 - 100 * len(titles),
                                 button_dimensions=button_size, action=self.game_map.create_graph, color=(255, 0, 0),
                                 font_size=24, font_name="Arial")

        load_to_json = MenuButton("Save Game", display_size[0] - 100, display_size[1] - 100 - 100 * 4,
                                  button_dimensions=button_size, action=self.save_game, color=(255, 0, 0),
                                  font_size=24, font_name="Arial")
        self.elements[0].append(finish_move)
        self.elements[0].append(load_to_json)
        print(self.elements)

    def subscribe_text_elements(self, observer, ):

        for element in self.lvl_2_elements:
            if isinstance(element, TextObservable):
                element.add_observer(observer)

    def check_click(self, mouse_pos: tuple[int, int]) -> bool:
        for layer in reversed(self.elements.values()):
            for element in layer:
                if element.visible and element.check_click(mouse_pos):
                    return True
        return False
