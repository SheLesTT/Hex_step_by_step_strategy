from math import sqrt

import pygame

from game_content.Sprites import Town


class MouseClickHandler:
    def __init__(self,game_map,  User_interface, tracker, mover):
        self.user_interface = User_interface
        self.game_map = game_map
        self.tracker = tracker
        self.mover = mover
        self.selected_sprite = None
        self.sprite_clicked = None
        self.unit_selected = None
        self.clicked_element = None
        self.hexes_available_move_selected_unit = []


    def handle_click(self, event):
        mouse_pos = event.dict["pos"]
        self.clicked_element =self.user_interface.check_click(mouse_pos)

        if not self.clicked_element:
            print("no element clicked")
            self.user_interface.hide_lvl_2_elements()
            self.check_hex_click(event)


    def add_hex(self, event):
        if selected_sprite_clicked := self.check_if_hex_is_clicked(event):
            hex_selected = self.user_interface.button_lists["hex_types"].selected_element
            self.game_map.change_hex(hex_selected, selected_sprite_clicked.grid_pos)

    def add_road(self, event):

        if selected_sprite_clicked := self.check_if_hex_is_clicked(event):
            selected_sprite_clicked.discover_what_roads_to_draw()

    def add_river(self, event):

        if selected_sprite_clicked := self.check_if_hex_is_clicked(event):
            mouse = self.get_real_mouse_pos(event)
            rect = self.get_hex_rectangle_with_offset(selected_sprite_clicked)
            local_x, local_y = self.calculate_mouse_pos_in_hex_rectangle(rect, mouse)

            triangle = self.check_which_triangle_was_clicked(local_x, local_y, selected_sprite_clicked)
            selected_sprite_clicked.discover_rivers_to_draw(triangle)

    def add_building(self, event):
        if selected_sprite_clicked := self.check_if_hex_is_clicked(event):
            print("Adding town")
            selected_sprite_clicked.add_building(Town(selected_sprite_clicked.grid_pos))

    def handle_click_in_none_mod(self, event):

        if selected_sprite_clicked := self.check_if_hex_is_clicked(event):
            if selected_sprite_clicked.building_on_hex:
                self.user_interface.open_element("city_surface")


    def check_hex_click(self, event):

        self.clear_selected_hexes()
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
                    self.add_building(event)
                case "None":
                    self.handle_click_in_none_mod(event)



        if event.button == 3:

            self.sprite_clicked = self.check_if_hex_is_clicked(event)
            if self.check_if_hex_is_clicked(event) and self.unit_selected :
                starting_sprite = self.selected_sprite.grid_pos
                ending_sprite = self.sprite_clicked.grid_pos

                available_pos= self.game_map.reachable_hexes(
                        self.selected_sprite.grid_pos, self.unit_selected.stamina)

                if ending_sprite in available_pos and self.player.moves > 0:
                    self.mover.move(starting_sprite, ending_sprite)
                    self.game_map.actions.append("<move"+str(starting_sprite)+ ","+str(ending_sprite)+">")
                    self.player.moves -= 1
                    self.unit_selected = None

        self.draw_selected_hexes()


    def clear_selected_hexes(self):

        for pos in self.hexes_available_move_selected_unit:
            cell_hex = self.game_map.get_hex_by_coord(pos)
            if cell_hex:
                cell_hex.draw()
        self.hexes_available_move_selected_unit = []
    def draw_selected_hexes(self):

        for pos in self.hexes_available_move_selected_unit:
            cell_hex = self.game_map.get_hex_by_coord(pos)
            if cell_hex:
                cell_hex.draw_in_unit_range()

    def check_if_rectangle_for_hex_was_clicked(self, sprite,  mouse_pos, offset):
        new_rec = pygame.Rect(offset.x + sprite.rect.x, offset.y + sprite.rect.y, sprite.rect.width, sprite.rect.height)
        if new_rec.collidepoint(mouse_pos.x, mouse_pos.y):
            return new_rec
        return False
    def check_which_triangle_was_clicked(self, local_x, local_y, sprite):

        local_x, local_y = local_x - sprite.width / 2, sprite.height - local_y - sprite.height / 2


        if local_y > 0 and local_x > 0 and local_y <= sqrt(3)* local_x:
            return 5
        if local_y > 0 and local_y >= sqrt(3) * local_x and local_y >= -sqrt(3) * local_x:
            return 4
        if local_y > 0 and local_x < 0 and local_y <= -sqrt(3) * local_x:
            return 3
        if local_y < 0 and local_x > 0 and local_y >= -sqrt(3) * local_x:
            return 0
        if local_y < 0 and local_y <= sqrt(3) * local_x and local_y <= -sqrt(3) * local_x:
            return 1
        if local_y < 0 and local_x < 0 and local_y >= sqrt(3) * local_x:
            return 2

    def get_real_mouse_pos(self, event):

        mouse = pygame.math.Vector2(event.pos)
        zoom=self.tracker.get_zoom()
        mouse *= 1 / zoom
        mouse += self.tracker.get_internal_offset()
        return  pygame.math.Vector2(int(mouse.x), int(mouse.y))

    def get_hex_rectangle_with_offset(self, sprite, ):

        offset = self.tracker.get_total_offset()
        return  pygame.Rect(offset.x + sprite.rect.x, offset.y + sprite.rect.y, sprite.rect.width, sprite.rect.height)

    def calculate_mouse_pos_in_hex_rectangle(self,rectangle, global_mouse_pos):
        local_x = int(global_mouse_pos.x) - rectangle.x
        local_y = int(global_mouse_pos.y) - rectangle.y
        return local_x, local_y
    def check_if_hex_is_clicked(self, event):
        mouse = self.get_real_mouse_pos(event)

        for sprite in self.game_map.hexes:
            new_rec = self.get_hex_rectangle_with_offset(sprite)
            if new_rec.collidepoint(mouse.x, mouse.y):
                local_x, local_y = self.calculate_mouse_pos_in_hex_rectangle(new_rec, mouse)
                if sprite.mask.get_at((local_x, local_y)):
                    return sprite



