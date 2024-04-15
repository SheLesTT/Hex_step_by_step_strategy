import pygame

from Modeling.CityGraph import CityGraph
from UI_staff.UI_Elements import MenuButton, UiSurface, ButtonList
from UI_staff.UI import UI


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
        self.add_hexes_list()

    def add_hexes_list(self):
        button_list = ButtonList(position=(200, 0), name="hex_types")
        hexes_types = ["Население", "Производство", "Продовольствие",]
        [button_list.add_element(hex_type, hex_type) for hex_type in hexes_types]
        self.add_element(0,button_list)
    def add_buttons(self,):

        display_size = pygame.display.get_surface().get_size()
        button_size = (100, 100)

        exit_button = MenuButton("Exit", 700,0, button_dimensions=button_size,
                                 action=None, color=(0, 0, 255), font_size=24, font_name="Arial",name = "exit")

        test_button= MenuButton("", 600,0, button_dimensions=button_size,
                                 action=None, color=(0, 0, 255), font_size=24, font_name="Arial",name = "parameter")
        start_simlation= MenuButton("mulation", display_size[0]-100, display_size[1]-100-100*4,
                                    button_dimensions=button_size, action=self.start_simulation, color=(255, 0, 0),
                                    font_size=24, font_name="Arial")

        self.add_element(0,start_simlation)
        self.add_element(0, exit_button)
        self.add_element(0, test_button)

    def add_surface(self):
        print("Calling add surface")
        surface = UiSurface(size=(300,800), position=(500,0),visible=False)
        surface.name = "city_surface"
        self.add_element(1,surface)


