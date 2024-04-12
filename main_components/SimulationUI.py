import pygame

from Modeling.CityGraph import CityGraph
from player_actions.UI_Elements import MenuButton, TextInput, UiSurface


class SimUI:
    def __init__(self, window_size, game_map, spawner):
        self.window_size = window_size
        self.UI_surface = None
        self.game_map = game_map
        self.spawner = spawner
        self.lvl_1_elements = []
        self.lvl_2_elements = []
        self.button_lists = {}
        self.init_elements()
        self.draw_elements()

    def start_simulation(self):
        graph = CityGraph(self.game_map)
        graph.run_simulation()
        # print("mulation")
    def init_elements(self):
        self.add_buttons()
        self.add_surface()


    def hide_lvl_2_elements(self):
        for element in self.lvl_2_elements:
            element.hide()
        self.draw_elements()
    def draw_elements(self):
        self.UI_surface = pygame.Surface(self.window_size, pygame.SRCALPHA)
        for element in self.lvl_1_elements:
            if element.visible:
                element.draw(self.UI_surface)
        for element in self.lvl_2_elements:
            if element.visible:
                element.draw(self.UI_surface)


    def add_buttons(self,):

        display_size = pygame.display.get_surface().get_size()
        button_size = (100, 100)

        start_simlation= MenuButton("mulation", display_size[0]-100, display_size[1]-100-100*4,
                                  button_dimensions=button_size, action=self.start_simulation, color=(255, 0, 0),
                                  font_size=24, font_name="Arial")

        self.lvl_1_elements.append(start_simlation)

    def add_surface(self):
        print("Calling add surface")
        surface = UiSurface(size=(300,800), position=(500,0),visible=False)
        surface.name = "city_surface"
        self.lvl_2_elements.append(surface)



    def subscribe_text_elements(self, observer, ):

        for element in self.lvl_2_elements:
            if isinstance(element, TextObservable):
                element.add_observer(observer)

    def find_element(self, name):
        for element in self.lvl_1_elements:
            if element.name == name:
                return element
        for element in self.lvl_2_elements:
            if element.name == name:
                return element

    def check_click(self, mouse_pos: tuple[int, int]) -> bool:
        for element in self.lvl_2_elements:
            if element.visible and element.check_click(mouse_pos):
                return True
        for element in self.lvl_1_elements:
            if element.visible and element.check_click(mouse_pos):
                return True
        return False
    def open_element(self, name):
        self.find_element(name).make_visible()
        self.draw_elements()
