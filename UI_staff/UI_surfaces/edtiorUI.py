import pygame

from UI_staff.UI_Elements import UiSurface, ButtonList, MenuButton, TextObservable
from UI_staff.UI import UI


class EditorUI(UI):
    def __init__(self, window_size, game_map,):
        super().__init__(window_size)
        self.UI_surface = None
        self.game_map = game_map
        self.active_list  = None
        self.init_elements()
        self.draw_elements()


    def save_game(self):
        self.game_map.save_to_json()

    def init_elements(self):
        self.add_buttons()
        self.add_hexes_list()
        self.add_editor_mods_list()
        self.add_surface()
        self.add_towns_list()


    def add_surface(self):
        surface = UiSurface(size=(300, 800), position=(500, 0), visible=False, name ="city_surface" )
        self.add_element(1,surface)

    def close_hexes_list(self):
        if self.active_list:
            self.active_list.hide()
            self.active_list = None

        self.draw_elements()

    def open_hexes_list(self, name:str):
        self.close_hexes_list()
        button_list = self.find_element(name)
        button_list.make_visible()
        self.draw_elements()
        self.active_list = button_list



    def add_hexes_list(self):
        button_list = ButtonList(position=(200, 0), name="hex_types")
        hexes_types = ["HexagonLand", "HexagonMountain", "HexagonSea", "HexagonEmpty", "HexagonForest", "HexagonSheep","HexagonWheat","HexagonGrape"]
        [button_list.add_element(hex_type, hex_type) for hex_type in hexes_types]
        self.add_element(0,button_list)
        button_list.hide()

    def add_editor_mods_list(self):
        button_list = ButtonList(position=(0, 0), name="editor_mods")
        modes = ["Hexes", "Rivers", "Roads", "Buildings", "None"]
        [button_list.add_element(mode, mode) for mode in modes]
        button_list.elements_list[1].add_action(self.close_hexes_list, action_args=())
        button_list.elements_list[2].add_action(self.close_hexes_list, action_args=())
        button_list.elements_list[4].add_action(self.close_hexes_list, action_args=())
        button_list.elements_list[0].add_action(self.open_hexes_list,action_args=("hex_types",))
        button_list.elements_list[3].add_action(self.open_hexes_list, action_args=("towns",))
        self.add_element(0,button_list)

    def add_towns_list(self):
        button_list = ButtonList(position=(200, 0), name="towns")
        modes = ["Town", "Village"]
        [button_list.add_element(mode, mode) for mode in modes]
        button_list.hide()
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
