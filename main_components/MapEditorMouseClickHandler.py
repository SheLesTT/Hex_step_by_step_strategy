from copy import copy
import pygame
import logging
from game_content.Sprites import Town, OffsetCoordinates
from typing import NamedTuple, Any

from main_components.MapMouseClickHandler import MapMouseClickHandler


class ActionRecord(NamedTuple):
    position: OffsetCoordinates
    action_type: str
    additional_info: Any


class MapEditorMouseClickHandler(MapMouseClickHandler):
    def __init__(self, game_map, user_interface, tracker):
        super().__init__(game_map, user_interface, tracker)
        self.clicked_element = None
        self.actions_list = []
        self.set_UI_buttons()


    def undo(self):
        print("i am in undo")
        if len(self.actions_list):
            action = self.actions_list.pop()
            if action.action_type == "hexagon":
                self.game_map.change_hex(action.additional_info, action.position)
            elif action.action_type == "river":
                self.game_map.hexes[action.position].remove_river(action.additional_info)
            elif action.action_type == "road":
                self.game_map.hexes[action.position].remove_road()

            # self.game_map.set_hex(hexagon, hexagon.grid_pos)

    def set_UI_buttons(self):
        self.user_interface.undo_button.add_action(self.undo, ())

    def handle_click(self, event):
        mouse_pos = event.dict["pos"]
        self.clicked_element = self.user_interface.check_click(mouse_pos)

        if not self.clicked_element:
            self.user_interface.hide_lvl_2_elements()
            self.check_hex_click(event)

    def add_hex(self, event):
        if selected_sprite_clicked := self.check_if_hex_is_clicked(event):
            hex_selected = self.user_interface.button_lists["hex_types"].selected_element
            self.actions_list.append(
                ActionRecord(selected_sprite_clicked.grid_pos, "hexagon", selected_sprite_clicked.type))
            print("list after save ", self.actions_list)
            self.game_map.change_hex(hex_selected, selected_sprite_clicked.grid_pos)

    def add_road(self, event):

        if selected_sprite_clicked := self.check_if_hex_is_clicked(event):
            selected_sprite_clicked.discover_what_roads_to_draw()
            self.actions_list.append(ActionRecord(selected_sprite_clicked.grid_pos, "road", None))

    def add_river(self, event):

        if selected_sprite_clicked := self.check_if_hex_is_clicked(event):
            mouse = self.get_real_mouse_pos(event)
            rect = self.get_hex_rectangle_with_offset(selected_sprite_clicked)
            local_x, local_y = self.calculate_mouse_pos_in_hex_rectangle(rect, mouse)

            triangle = self.check_which_triangle_was_clicked(local_x, local_y, selected_sprite_clicked)
            selected_sprite_clicked.discover_rivers_to_draw(triangle)
            self.actions_list.append(ActionRecord(selected_sprite_clicked.grid_pos, "river", triangle))

    def add_building(self, event):
        if selected_sprite_clicked := self.check_if_hex_is_clicked(event):
            selected_sprite_clicked.add_building(Town(selected_sprite_clicked.grid_pos))
            self.actions_list.append(copy(selected_sprite_clicked))

    def handle_click_in_none_mod(self, event):

        if selected_sprite_clicked := self.check_if_hex_is_clicked(event):
            if selected_sprite_clicked.building_on_hex:
                self.user_interface.find_element("city_surface").set_city(selected_sprite_clicked.building_on_hex)
                self.user_interface.open_element("city_surface")

    def check_hex_click(self, event):

        mouse = pygame.math.Vector2(pygame.mouse.get_pos())
        mouse -= self.tracker.get_dragging_offset()

        if event.button == 1:

            match self.user_interface.button_lists["editor_mods"].selected_element:
                case "Hexes":
                    self.add_hex(event)
                case "Rivers":
                    self.add_river(event)
                case "Roads":
                    self.add_road(event)
                case "Buildings":
                    print("Clicked building")
                    self.add_building(event)

                case "None":
                    self.handle_click_in_none_mod(event)


