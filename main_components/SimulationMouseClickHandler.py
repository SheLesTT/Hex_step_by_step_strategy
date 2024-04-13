import pygame
from game_content.Sprites import Town
from main_components.MapMouseClickHandler import MapMouseClickHandler

class SimulationMouseClickHandler(MapMouseClickHandler):
    def __init__(self, game_map, user_interface, tracker):
        super().__init__(game_map, user_interface, tracker)
        self.sprite_clicked = None
        self.clicked_element = None

    def handle_click(self, event):
        mouse_pos = event.dict["pos"]
        self.clicked_element = self.user_interface.check_click(mouse_pos)

        if not self.clicked_element:
            self.user_interface.hide_lvl_2_elements()
            self.check_hex_click(event)

    def handle_click_in_none_mod(self, event):
        if selected_sprite_clicked := self.check_if_hex_is_clicked(event):
            if selected_sprite_clicked.building_on_hex:
                self.user_interface.find_element("city_surface").set_city(selected_sprite_clicked.building_on_hex)
                self.user_interface.open_element("city_surface")

    def check_hex_click(self, event):

        mouse = pygame.math.Vector2(pygame.mouse.get_pos())
        mouse -= self.tracker.get_dragging_offset()

        if event.button == 1:
            self.handle_click_in_none_mod(event)

