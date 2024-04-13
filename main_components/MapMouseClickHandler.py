from abc import ABC, abstractmethod
import pygame
from math import sqrt

class MapMouseClickHandler(ABC):
    def __init__(self, game_map, user_interface, tracker):
        self.game_map = game_map
        self.user_interface = user_interface
        self.game_map = game_map
        self.tracker = tracker

    @abstractmethod
    def handle_click(self):
        pass

    def check_which_triangle_was_clicked(self, local_x, local_y, sprite):

        local_x, local_y = local_x - sprite.width / 2, sprite.height - local_y - sprite.height / 2

        if local_y > 0 and local_x > 0 and local_y <= sqrt(3) * local_x:
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
        zoom = self.tracker.get_zoom()
        mouse *= 1 / zoom
        mouse += self.tracker.get_internal_offset()
        return pygame.math.Vector2(int(mouse.x), int(mouse.y))

    def get_hex_rectangle_with_offset(self, sprite, ):

        offset = self.tracker.get_total_offset()
        return pygame.Rect(offset.x + sprite.rect.x, offset.y + sprite.rect.y, sprite.rect.width, sprite.rect.height)

    def calculate_mouse_pos_in_hex_rectangle(self, rectangle, global_mouse_pos):
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
                    print("Sprite clicked:", sprite.grid_pos, sprite.building_on_hex)
                    return sprite
