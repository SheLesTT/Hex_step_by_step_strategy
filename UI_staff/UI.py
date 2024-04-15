import os

from Modeling.CityGraph import CityGraph
from UI_staff.UI_Elements import *
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



