from typing import NoReturn
from abc import ABC, abstractmethod
import pygame, sys

from main_components.Map import Map


def empty_funciton():
    print("")

class UI_Element(ABC):
    def __init__(self):
        self.visible = True
        self.name = ""

    @abstractmethod
    def draw(self, pygame_surface: pygame.Surface) -> None:
        pass

    def hide(self):
        self.visible = False

    def make_visible(self):
        self.visible = True
class Button(UI_Element):
    def __init__(self, text, x, y, button_dimensions: tuple[int, int],x_offset = 0, y_offset = 0,
                 action = empty_funciton, color:tuple[int, int, int]=(0, 255, 0),
                 font_size:int = 24, font_name:str ="Arial",):
        super().__init__()
        self.rect = pygame.Rect(x, y, button_dimensions[0], button_dimensions[1])

        self.text = text
        self.color = color
        self.action = action
        font = pygame.font.SysFont(font_name, font_size)
        self.text_surf = font.render(text, True, '#FFFFFF')
        self.text_rect = self.text_surf.get_rect(center=self.rect.center)
        # self.is_clickable = False

    # def reset_clickability(self):
    #     self.is_clickable = True

    def draw(self, display_surface: pygame.Surface) -> None:
        if self.visible == True:
            pygame.draw.rect(display_surface, self.color, self.rect)
            pygame.draw.rect(display_surface, "Black", self.rect, 2)
            display_surface.blit(self.text_surf, self.text_rect)

    @abstractmethod
    def check_click(self,pos) -> bool:
        pass


class MenuButton(Button):
    def __init__(self, text, x, y,button_dimensions: tuple[int, int],x_offset =0, y_offset = 0,
                 action = empty_funciton,action_args= (),
                 color=(0, 255, 0), font_size=24, font_name="Arial",  ):
        super().__init__(text, x, y,button_dimensions , x_offset=x_offset, y_offset= y_offset, action= action, color=color, font_size = font_size, font_name = font_name)
        self.x_offset = x_offset
        self.y_offset = y_offset
        self.action = action
        self.action_args = action_args
        self.button_dimensions = button_dimensions
        self.abs_x = x + x_offset
        self.abs_y = y + y_offset
        self.absolute_rect = pygame.Rect(self.abs_x, self.abs_y, self.button_dimensions[0], self.button_dimensions[1])

    def check_click(self, pos: tuple[int, int]):

        if  self.absolute_rect.collidepoint(pos):
                self.action(*self.action_args)
                return self
        return False
    def move_button(self, offset):
        self.y_offset += offset
        self.abs_y += offset
        self.absolute_rect = pygame.Rect(self.abs_x, self.abs_y, self.button_dimensions[0], self.button_dimensions[1])



class ButtonList(UI_Element):
    def __init__(self,bottom_surface_size: tuple[int, int] = (200, 400),
                 upper_surface_size: tuple[int, int]= (200,200),
                 upper_surface_color: tuple[int, int, int] = (255, 255, 0),
                 position: tuple[int, int] = (0,0),
                 button_dimensions: tuple[int, int] = (180, 35),
                 new_element_top_left_corner: tuple[int, int] = (10,10),):
        super().__init__()
        self.bottom_surf = pygame.Surface(bottom_surface_size, pygame.SRCALPHA)
        # self.but_rect = self.bottom_surf.get_rect(topleft=(0,0))
        self.upper_surf = pygame.Surface( upper_surface_size, pygame.SRCALPHA)
        self.upper_surf_color = upper_surface_color
        self.upper_surf.blit(self.bottom_surf,(0,0))
        self.upper_surf.fill(self.upper_surf_color)
        self.x_offset = position[0]
        self.y_offset = position[1]
        self.new_element_top_left_corner_x = new_element_top_left_corner[0]
        self.new_element_top_left_corner_y = new_element_top_left_corner[1]
        self.absolute_rect = pygame.Rect(self.x_offset, self.y_offset, 200, 300)
        self.button_dimensions = button_dimensions
        self.elements = {}
        self.selected_element = None
        self.scroll = 0
        # self.offset_x = offset_x


    def add_element(self,button_text,element_to_choose):

        game_button = MenuButton(button_text, self.new_element_top_left_corner_x, self.new_element_top_left_corner_y,
                                 self.button_dimensions, x_offset=self.x_offset, y_offset=self.y_offset,)
        game_button.draw(self.bottom_surf)

        self.upper_surf.blit(self.bottom_surf,(0,self.scroll))
        self.elements[game_button] = element_to_choose
        self.new_element_top_left_corner_y += 40

    def check_scroll(self,y):
        mouse_pos = pygame.mouse.get_pos()
        if  self.absolute_rect.collidepoint(mouse_pos):

            test_scroll = self.scroll + y*10
            if test_scroll< 0 and  test_scroll> - (self.bottom_surf.get_height() - self.upper_surf.get_height()):
                self.scroll = test_scroll
                self.upper_surf.fill(self.upper_surf_color)
                self.upper_surf.blit(self.bottom_surf,(0,self.scroll))
                [element.move_button(y*10) for element in self.elements]
    def check_click(self, mouse_pos: tuple[int, int]):


        for element in self.elements:
            if element.check_click(mouse_pos):
                self.selected_element = self.elements[element]
                return self
    def draw(self, display_surface: pygame.Surface):
        if self.visible:
            display_surface.blit(self.upper_surf, (self.x_offset, self.y_offset))


class TextInput(UI_Element):
    def __init__(self, text = None):
        super().__init__()
        self.text = text
        self.font = pygame.font.SysFont("Arial", 24)
        self.text_surf = self.font.render(self.text, True, '#FFFFFF')
        self.surf = pygame.Surface((200, 50))

    def draw(self, display_surface: pygame.Surface):
        if self.visible:
            self.surf.blit(self.text_surf, (0,0))
            display_surface.blit(self.text_surf, (10, 10))

class UiSurface(UI_Element):
    def __init__(self, size: tuple[int, int], position: tuple[int, int]):
        super().__init__()
        self.surface = pygame.Surface(size, masks=(0,0,0))
        self.position = position


    def draw(self, display_surface: pygame.Surface):
        if self.visible:

            display_surface.blit(self.surface, self.position)





