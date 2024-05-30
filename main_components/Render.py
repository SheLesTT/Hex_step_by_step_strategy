import pygame

from game_content.Sprites import Mine


class Render:
    def __init__(self, internal_surface_size, map_movement_tracker, user_interface):
        self.map_movement_tracker = map_movement_tracker
        self.user_interface = user_interface
        self.internal_surface = pygame.Surface(internal_surface_size, pygame.SRCALPHA)
        self.display_surface = pygame.display.get_surface()
        self.display_surface.fill((0,0,23))
        self.internal_surface_rect = self.internal_surface.get_rect(
            center=(self.display_surface.get_size()[0] // 2, self.display_surface.get_size()[1] // 2))




    def pre_display(self, events_list):

        self.internal_surface.fill((0, 0, 0, 0))
        self.map_movement_tracker.screen_movement_with_mouse_dragging(events_list)
        self.display_surface.fill((255, 255, 255))  # #71deee initial background color

    def display_hexes(self, sprite_group: pygame.sprite.Group) -> None:
        offset = self.map_movement_tracker.get_total_offset()
        for sprite in sprite_group.sprites():
            self.internal_surface.blit(sprite.image, offset + sprite.rect.topleft)


    def display_surfaces(self):
        scaled_surface = pygame.transform.smoothscale(self.internal_surface,
                                                      self.map_movement_tracker.get_internal_surface_scale())
        scaled_rect = scaled_surface.get_rect(center=self.internal_surface_rect.center)
        self.display_surface.blit(scaled_surface, (scaled_rect[0], scaled_rect[1]))
        self.display_surface.blit(self.user_interface.UI_surface, (0, 0))

    def display(self, events_list, game_map, ):

        self.pre_display(events_list)
        self.display_hexes(game_map.hexes)
        self.display_surfaces()

