import pygame
from colors import Color as C
from Modeling.CityGraph import CityGraph
from UI_staff.UI_Elements import MenuButton, UiSurface, ButtonList, ParametersSurface
from UI_staff.UI import UI


class SimUI(UI):
    def __init__(self, window_size, game_map,):
        super().__init__(window_size)
        self.window_size = window_size
        self.game_map = game_map
        self.global_parameters = {"population":0, "food":0, "goods":0, "year":1200, "modeling_speed":1}
        self.init_elements()
        self.draw_elements()
        self.curren_speed = 1

    def start_simulation(self):
        graph = CityGraph(self.game_map, self)
        graph.run_simulation()
        # print("mulation")
    def init_elements(self):
        self.add_surface()
        self.add_hexes_list()
        self.add_parameter_surface()
        self.subscribe_to_global_parameters()

        self.add_buttons()

    def subscribe_to_global_parameters(self, ):
        self.game_map.global_parameters.add_observer(self)

    def update_parameter_surface(self):
        surface = self.find_element("parameters_surface")
        surface["population_val"].change_text(str(self.global_parameters["population"]))
        surface["modeling_speed_val"].change_text(str(self.global_parameters["modeling_speed"]))
        surface["year_val"].change_text(str(self.global_parameters["year"]))
        surface.draw(self.UI_surface)
    def update(self, parameter, value):
        self.global_parameters[parameter] = value
        self.update_parameter_surface()



    def add_parameter_surface(self):
        surface = ParametersSurface(size=(800,100), position=(0,0),visible=True, name="parameters_surface")
        self.add_element(0,surface)

    def add_hexes_list(self):
        button_list = ButtonList(position=(0, 100), name="parameters")
        hexes_types = ["Население", "Производство", "Продовольствие",   "Отмена"]
        selected_parameters = ["population", "cattle","population", None]
        [button_list.add_element(button_name, parameter) for button_name, parameter in zip(hexes_types, selected_parameters)]
        button_list.elements_list[0].add_action(self.visualize_param, action_args=("population",))
        button_list.elements_list[1].add_action(self.visualize_param, action_args=("goods",))
        button_list.elements_list[2].add_action(self.visualize_param, action_args=("food",))
        button_list.elements_list[3].add_action(self.visualize_param, action_args=())


        self.add_element(0,button_list)
    def speed_up(self):
        with open("speed.txt", "w") as file:
            if self.curren_speed < 16:
                self.curren_speed *= 2
            file.write(str(self.curren_speed))
    def slow_down(self):
        with open("speed.txt", "w") as file:
            if self.curren_speed > 1/16:
                self.curren_speed /= 2
            file.write(str(self.curren_speed))
    def add_buttons(self,):

        display_size = pygame.display.get_surface().get_size()
        button_size = (60, 60)
        cross_image = pygame.image.load('Resources/cross.png')
        cross_image = pygame.transform.scale(cross_image, (50,50))
        exit_button = MenuButton("Exit", 700,0, button_dimensions=button_size,
                                 action=None, color=(0, 0, 255), font_size=24, font_name="Arial",name = "exit",image=cross_image)

        speed_up_button = MenuButton("Speed up", 600,0, button_dimensions=button_size,
                                 action=self.speed_up, color=(0, 0, 255), font_size=24, font_name="Arial",name = "parameter", image='Resources/faster.png')
        slow_down_button = MenuButton("Slow down", 500,0, button_dimensions=button_size,
                                action=self.slow_down, color=(0, 0, 255), font_size=24, font_name="Arial",name = "parameter",image='Resources/slower.png')
        start_simulation= MenuButton("Cтарт", 700,700 ,
                                    button_dimensions=(100,100), action=self.start_simulation, color=(C.yellow),
                                    font_size=24, font_name="Arial", name="start_simulation", )
        start_simulation.add_action(self.start_simulation)
        self.add_element(0,start_simulation)
        self["parameters_surface"].add_element(0,exit_button)
        self["parameters_surface"].add_element(0,speed_up_button)
        self["parameters_surface"].add_element(0,slow_down_button)
    def visualize_param(self, parameter = None):
        self.game_map.visualize_parameters(parameter)
    def add_surface(self):
        surface = UiSurface(size=(300,800), position=(500,0),visible=False)
        surface.name = "city_surface"
        self.add_element(1,surface)


