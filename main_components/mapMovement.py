import pygame


class MapMovementTracker(pygame.sprite.Group):
    def __init__(self, internal_surface_size, display_surface_size):
        super().__init__()
        self.internal_surface_size = internal_surface_size
        self.internal_surface_size_vector = pygame.math.Vector2(internal_surface_size)
        self.display_surface_size = display_surface_size

        self.offset = pygame.math.Vector2(0, 0)
        self.display_surface_half_width = self.display_surface_size[0] // 2
        self.display_surface_half_height = self.display_surface_size[1] // 2

        self.mouse_speed = 0.4

        # camera control
        self.mouse_pos_down = pygame.math.Vector2(0, 0)
        self.mouse_pos_up = pygame.math.Vector2(0, 0)
        self.drag_flag = False

        # zoom
        self.zoom_scale = 1

        self.internal_surface_size_vector = pygame.math.Vector2(self.internal_surface_size)
        self.internal_offset = pygame.math.Vector2(0, 0)
        self.internal_offset.x = self.internal_surface_size[0] // 2 - self.display_surface_half_width
        self.internal_offset.y = self.internal_surface_size[1] // 2 - self.display_surface_half_height

        self.offset_borders = {"left": -self.internal_offset.x,
                               "right": self.internal_surface_size[0] - self.display_surface_size[0],
                               "top": self.internal_surface_size[1] - self.display_surface_size[1],
                               "bottom": -self.internal_offset.y}

    def screen_movement_with_mouse_dragging(self, events_list):

        for event in events_list:
            # controlling zoom
            if event.type == pygame.MOUSEWHEEL:
                self.change_zoom(event)

            if event.type == pygame.MOUSEBUTTONDOWN:
                self.start_dragging()

            if self.drag_flag:
                self.handle_dragging(event)

    def change_zoom(self, event):
        self.zoom_scale += event.y * 0.03
        if self.zoom_scale > 1.25 and event.y > 0:
            self.zoom_scale = 1.25
        if self.zoom_scale < 0.75 and event.y < 0:
            self.zoom_scale = 0.75

    def is_offset_in_borders(self, offset_borders):
        if self.offset.x < offset_borders['left']:
            self.offset.x = offset_borders['left']
        if self.offset.x > offset_borders['right']:
            self.offset.x = offset_borders['right']
        if self.offset.y < offset_borders['bottom']:
            self.offset.y = offset_borders['bottom']
        if self.offset.y > offset_borders['top']:
            self.offset.y = offset_borders['top']

    def start_dragging(self):
        self.mouse_pos_down = pygame.math.Vector2(pygame.mouse.get_pos())
        self.drag_flag = True

    def handle_dragging(self, event):
        mouse_pos_up = pygame.math.Vector2(pygame.mouse.get_pos())

        self.check_minimal_mouse_movement_for_dragging(10, mouse_pos_up)

        if event.type == pygame.MOUSEBUTTONUP:
            self.drag_flag = False
        self.mouse_pos_down = mouse_pos_up

    def check_minimal_mouse_movement_for_dragging(self, minimal_mouse_movement, mouse_pos_up):
        if mouse_pos_up.distance_to(self.mouse_pos_down) > minimal_mouse_movement:
            self.offset += (mouse_pos_up - self.mouse_pos_down) * self.mouse_speed

            self.is_offset_in_borders(self.offset_borders)

    def get_total_offset(self):
        return self.offset + self.internal_offset

    def get_dragging_offset(self):
        return self.offset

    def get_internal_offset(self):
        zoom_scale = self.get_zoom()
        internal_offset = pygame.math.Vector2(0, 0)
        internal_offset.x = self.internal_surface_size[0] // 2 - self.display_surface_half_width * (1 / zoom_scale)
        internal_offset.y = self.internal_surface_size[1] // 2 - self.display_surface_half_height * (1 / zoom_scale)
        return internal_offset

    def get_internal_surface_scale(self):

        return self.zoom_scale * self.internal_surface_size_vector

    def get_zoom(self):
        return self.zoom_scale
