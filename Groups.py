import pygame

class CameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()


        self.offset = pygame.math.Vector2(0,0)
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2

        # moving camera with mouse
        self.camera_borders = {'left':10, 'right':10, 'top':10, 'bottom':10}
        l = self.camera_borders['left']
        r = self.camera_borders['top']
        w = self.display_surface.get_size()[0] -(self.camera_borders['right'] + self.camera_borders['left'])
        h = self.display_surface.get_size()[1] -(self.camera_borders['bottom'] + self.camera_borders['top'])
        self.camera_rect = pygame.Rect(l, r, w, h)

        self.mouse_speed= 0.4

        # camera control
        self.mouse_pos_down = pygame.math.Vector2(0,0)
        self.mouse_pos_up = pygame.math.Vector2(0,0)
        self.drag_flag = False

        # zoom
        self.zoom_scale = 1
        self.internal_surface_size= (2000, 2000)

        self.internal_surface = pygame.Surface(self.internal_surface_size, pygame.SRCALPHA)

        pygame.draw.rect(self.internal_surface,"yellow",(1,1,2300,2300),3)
        # creating internal surface centered with display surface
        self.internal_rect = self.internal_surface.get_rect(center = (self.half_width, self.half_height))
        self.internal_surface_size_vector = pygame.math.Vector2(self.internal_surface_size)
        self.internal_offset = pygame.math.Vector2(0,0)
        self.internal_offset.x = self.internal_surface_size[0]//2 - self.half_width
        self.internal_offset.y = self.internal_surface_size[1]//2 - self.half_height




    def screen_movement_with_mouse_dragging(self, events_list):

        for event in events_list:
            # controlling zoom
            if event.type == pygame.MOUSEWHEEL:
                if (self.zoom_scale < 1.75 and event.y >0) or (self.zoom_scale>0.65 and event.y < 0):
                    self.zoom_scale += event.y * 0.03

            if event.type == pygame.MOUSEBUTTONDOWN:

                self.mouse_pos_down = pygame.math.Vector2(pygame.mouse.get_pos())
                self.drag_flag = True


            if self.drag_flag:
                mouse_pos_up = pygame.math.Vector2(pygame.mouse.get_pos())

                if mouse_pos_up.distance_to(self.mouse_pos_down) > 10:
                    print(self.display_surface)
                    print(self.internal_surface)
                    print(self.internal_offset)
                    self.offset+= (mouse_pos_up - self.mouse_pos_down) * self.mouse_speed
                    if self.offset.x < -self.internal_offset.x:
                        self.offset.x= -self.internal_offset.x
                    if self.offset.x > self.internal_surface.get_size()[0] - self.display_surface.get_size()[0] :
                        self.offset.x = self.internal_surface.get_size()[0] - self.display_surface.get_size()[0]
                    if self.offset.y < -self.internal_offset.y:
                        self.offset.y=-self.internal_offset.y
                    if self.offset.y > self.internal_surface.get_size()[1] - self.display_surface.get_size()[1] :
                        self.offset.y = self.internal_surface.get_size()[1] - self.display_surface.get_size()[1]

                if event.type == pygame.MOUSEBUTTONUP:
                    self.drag_flag = False
                self.mouse_pos_down = mouse_pos_up

    def screen_mouse_control_with_moving(self):
        mouse = pygame.math.Vector2(pygame.mouse.get_pos())
        mouse_offset_vector = pygame.math.Vector2(0,0)

        left_border = self.camera_borders['left']
        top_border = self.camera_borders['top']
        right_border = self.display_surface.get_size()[0] - self.camera_borders['right']
        bottom_border = self.display_surface.get_size()[1] - self.camera_borders['bottom']

        if top_border < mouse.y < bottom_border:
            if mouse.x < left_border:
                mouse_offset_vector.x = mouse.x - left_border
                pygame.mouse.set_pos((left_border, mouse.y))
            if mouse.x > right_border:
                mouse_offset_vector.x =  mouse.x - right_border
                pygame.mouse.set_pos((right_border, mouse.y))

        elif mouse.y < top_border:
            if mouse.x < left_border:
                mouse_offset_vector = mouse - pygame.math.Vector2(left_border, top_border)
                print(mouse_offset_vector)
                pygame.mouse.set_pos((left_border, top_border))
            if mouse.x > right_border:
                mouse_offset_vector = mouse - pygame.math.Vector2(right_border, top_border)
                pygame.mouse.set_pos((right_border, top_border))


        if left_border < mouse.x < right_border:
            if mouse.y < top_border:
                mouse_offset_vector.y = mouse.y - top_border
                pygame.mouse.set_pos((mouse.x, top_border))
            if mouse.y > bottom_border:
                mouse_offset_vector.y =  mouse.y - bottom_border
                pygame.mouse.set_pos((mouse.x, bottom_border))

        elif mouse.y > bottom_border:
            if mouse.x < left_border:
                mouse_offset_vector = mouse - pygame.math.Vector2(left_border, bottom_border)
                pygame.mouse.set_pos((left_border, bottom_border))
            if mouse.x > right_border:
                mouse_offset_vector = mouse - pygame.math.Vector2(right_border, bottom_border)
                pygame.mouse.set_pos((right_border, bottom_border))
        self.offset -= mouse_offset_vector *self.mouse_speed

    def custom_draw(self, events_list):
        # self.mouse_control()
        self.screen_movement_with_mouse_dragging(events_list)

        self.internal_surface.fill('#71deee')
        for sprite in self.sprites():
            offset_pos = sprite.rect.topleft + self.offset + self.internal_offset
            self.internal_surface.blit(sprite.image, offset_pos)

        scaled_surface = pygame.transform.scale(self.internal_surface, self.internal_surface_size_vector * self.zoom_scale)
        scaled_rect = scaled_surface.get_rect(center = self.internal_rect.center)


        self.display_surface.blit(scaled_surface,scaled_rect)

