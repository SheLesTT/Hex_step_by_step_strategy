from copy import copy
import pygame
import logging
from game_content.Sprites import Town, OffsetCoordinates, Village
from typing import NamedTuple, Any

from main_components.MapMouseClickHandler import MapMouseClickHandler


class ActionRecord(NamedTuple):
    position: OffsetCoordinates
    action_type: str
    additional_info: Any
    delete: bool = False


class MapEditorMouseClickHandler(MapMouseClickHandler):
    def __init__(self, game_map, user_interface, tracker):
        super().__init__(game_map, user_interface, tracker)
        self.clicked_element = None
        self.actions_list = []
        self.delete_mode = False
        self.set_UI_buttons()

    def undo(self):
        if len(self.actions_list):
            action = self.actions_list.pop()
            self.logger.debug(f"undoing action {action}")
            if action.action_type == "hexagon":
                self.game_map.change_hex(action.additional_info, action.position)
            elif action.action_type == "river":
                if not action.delete:
                    self.game_map.hexes[action.position].remove_river(action.additional_info)
                else:
                    self.add_river(action.additional_info,self.game_map.hexes[action.position],True)
            elif action.action_type == "road":
                if not action.delete:
                    self.game_map.hexes[action.position].remove_road()
                else:
                    self.add_road(self.game_map.hexes[action.position], True)
            elif action.action_type == "building":
                if not action.delete:
                    self.game_map.hexes[action.position].remove_building()
                else:
                    self.add_building(self.game_map.hexes[action.position],action.additional_info, True)

    def change_delete_mod(self):
        self.delete_mode = not self.delete_mode

    def set_UI_buttons(self):
        self.user_interface.find_element("undo").add_action(self.undo, ())
        self.user_interface.find_element("delete").add_action(self.change_delete_mod, ())

    def handle_click(self, event):
        mouse_pos = event.dict["pos"]
        self.clicked_element = self.user_interface.check_click(mouse_pos)

        if not self.clicked_element:
            self.user_interface.hide_layer_elements(1)
            self.check_hex_click(event)

    def add_hex(self, sprite_clicked):
        hex_selected = self.user_interface.find_element("hex_types").selected_element
        self.game_map.change_hex(hex_selected, sprite_clicked.grid_pos)
        self.actions_list.append(ActionRecord(sprite_clicked.grid_pos, "hexagon", sprite_clicked.type))
        self.logger.info(f"Added hex, {sprite_clicked.grid_pos}, hexagon, {sprite_clicked.type}")

    def add_road(self, sprite_clicked, undoing=False):
        sprite_clicked.discover_what_roads_to_draw()
        if not undoing:
            self.actions_list.append(ActionRecord(sprite_clicked.grid_pos, "road", None))
        self.logger.info(f"Added road, {sprite_clicked.grid_pos}, road")

    def del_road(self, sprite_clicked, undoing = False):
        sprite_clicked.remove_road()
        if not undoing:
            self.actions_list.append(ActionRecord(sprite_clicked.grid_pos, "road", None, True))

    def which_triangle_was_clicked(self, event, sprite_clicked):
        mouse = self.get_real_mouse_pos(event)
        rect = self.get_hex_rectangle_with_offset(sprite_clicked)
        local_x, local_y = self.calculate_mouse_pos_in_hex_rectangle(rect, mouse)

        return self.check_which_triangle_was_clicked(local_x, local_y, sprite_clicked)

    def add_river(self, event: pygame.event.Event | int , sprite_clicked, undoing=False):
        if isinstance(event, pygame.event.Event):
            triangle = self.which_triangle_was_clicked(event, sprite_clicked)
        else:
            triangle = event
        sprite_clicked.discover_rivers_to_draw(triangle)
        if not undoing:
            self.actions_list.append(ActionRecord(sprite_clicked.grid_pos, "river", triangle))
        self.logger.info(f"Added road, {sprite_clicked.grid_pos}, river, {triangle}")

    def del_river(self, event, sprite_clicked, undoing=False):
        triangle = self.which_triangle_was_clicked(event, sprite_clicked)
        sprite_clicked.remove_river(triangle)
        if not undoing:
            self.actions_list.append(ActionRecord(sprite_clicked.grid_pos, "river", triangle, True))

    def add_building(self, sprite_clicked, building_type, undoing=False):
        game_map = sprite_clicked.game_map
        available_hexes = game_map.coordinate_range(sprite_clicked, 1)
        if building_type == "Town":
            building = Town(sprite_clicked.grid_pos,game_map)
        if building_type == "Village":
            building = Village(sprite_clicked.grid_pos, game_map)

        sprite_clicked.add_building(building)
        if not undoing:
            self.actions_list.append(ActionRecord(sprite_clicked.grid_pos, "building", building_type))
        self.logger.info(f"Added building, {sprite_clicked.grid_pos}, building")

    def del_building(self, sprite_clicked, undoing=False):
        building_name = sprite_clicked.building_on_hex.name
        sprite_clicked.remove_building()
        if not undoing:
            self.actions_list.append(ActionRecord(sprite_clicked.grid_pos, "building", building_name, True))

    def handle_click_in_none_mod(self, sprite_clicked):
        print("handling click in none mod")
        if sprite_clicked.building_on_hex:
            self.logger.debug("Clicked o a hex with a building in none mode")
            self.user_interface.find_element("city_surface").set_city(sprite_clicked.building_on_hex)
            self.user_interface.open_element("city_surface")

    def check_hex_click(self, event):

        mouse = pygame.math.Vector2(pygame.mouse.get_pos())
        mouse -= self.tracker.get_dragging_offset()

        if event.button == 1:
            print("go click event")
            if sprite_clicked := self.check_if_hex_is_clicked(event):
                print("sprite clicked", sprite_clicked)

                print("Editor mod selected", self.user_interface.find_element("editor_mods").selected_element)
                match self.user_interface.find_element("editor_mods").selected_element:
                    case "Hexes":
                        if not self.delete_mode:
                            print("Adding hex, self delete mode", self.delete_mode)
                            self.add_hex(sprite_clicked)
                    case "Rivers":
                        if not self.delete_mode:
                            self.add_river(event, sprite_clicked)
                        else:
                            self.del_river(event, sprite_clicked)
                    case "Roads":
                        if not self.delete_mode:
                            self.add_road(sprite_clicked)
                        else:
                            self.del_road(sprite_clicked)
                    case "Buildings":
                        if not self.delete_mode:
                            building_type = self.user_interface.find_element("towns").selected_element
                            self.add_building(sprite_clicked, building_type)
                        else:
                            self.del_building(sprite_clicked)

                    case "None":
                        self.handle_click_in_none_mod(sprite_clicked)
