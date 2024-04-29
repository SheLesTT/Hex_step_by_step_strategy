from abc import ABC, abstractmethod
import pygame, sys


def empty_funciton():
    pass


class Observable:
    def __init__(self):
        self.observers = []

    def add_observer(self, observer):
        pass

    def remove_observer(self):
        pass

    def notify_observers(self):
        pass


class TextObservable(Observable):

    def __init__(self):
        super().__init__()
        self.observers = []

    pass


class UI_Element(ABC):
    def __init__(self, name):
        self.visible = True
        self.name = name

    @abstractmethod
    def draw(self, pygame_surface: pygame.Surface) -> None:
        pass

    def hide(self):
        self.visible = False

    def make_visible(self):
        self.visible = True


class Scrollable:
    @abstractmethod
    def check_scroll(self, scroll):
        pass


class Button(UI_Element):
    def __init__(self, text, x, y, button_dimensions: tuple[int, int], name="", x_offset=0, y_offset=0,
                 action=empty_funciton, color: tuple[int, int, int] = (0, 255, 0),
                 font_size: int = 24, font_name: str = "Arial", ):
        super().__init__(name=name)
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
    def check_click(self, pos) -> bool:
        pass


class MenuButton(Button):
    def __init__(self, text, x, y, button_dimensions: tuple[int, int], x_offset=0, y_offset=0,
                 action=empty_funciton, action_args=(),
                 color=(0, 255, 0), font_size=24, font_name="Arial", name=""):
        super().__init__(text, x, y, button_dimensions, x_offset=x_offset, y_offset=y_offset, action=action,
                         color=color, font_size=font_size, font_name=font_name, name=name)
        self.x_offset = x_offset
        self.y_offset = y_offset
        self.action = action
        self.action_args = action_args
        self.button_dimensions = button_dimensions
        self.abs_x = x + x_offset
        self.abs_y = y + y_offset
        self.absolute_rect = pygame.Rect(self.abs_x, self.abs_y, self.button_dimensions[0], self.button_dimensions[1])

    def check_click(self, pos: tuple[int, int]):
        if self.absolute_rect.collidepoint(pos):
            print("Button was clicked ", self.action, pos, self.absolute_rect)
            self.action(*self.action_args)
            return True
        return False

    def add_action(self, action, action_args=()):
        self.action = action
        self.action_args = action_args

    def move_button(self, offset):
        self.y_offset += offset
        self.abs_y += offset
        self.absolute_rect = pygame.Rect(self.abs_x, self.abs_y, self.button_dimensions[0], self.button_dimensions[1])


class ButtonList(UI_Element, Scrollable):
    def __init__(self, bottom_surface_size: tuple[int, int] = (200, 400),
                 upper_surface_size: tuple[int, int] = (200, 200),
                 upper_surface_color: tuple[int, int, int] = (255, 255, 0),
                 position: tuple[int, int] = (0, 0),
                 button_dimensions: tuple[int, int] = (180, 35),
                 new_element_top_left_corner: tuple[int, int] = (10, 10),
                 name=""):
        super().__init__(name)
        self.bottom_surf = pygame.Surface(bottom_surface_size, pygame.SRCALPHA)
        # self.but_rect = self.bottom_surf.get_rect(topleft=(0,0))
        self.upper_surf = pygame.Surface(upper_surface_size, pygame.SRCALPHA)
        self.upper_surf_color = upper_surface_color
        self.upper_surf.blit(self.bottom_surf, (0, 0))
        self.upper_surf.fill(self.upper_surf_color)
        self.x_offset = position[0]
        self.y_offset = position[1]
        self.new_element_top_left_corner_x = new_element_top_left_corner[0]
        self.new_element_top_left_corner_y = new_element_top_left_corner[1]
        self.absolute_rect = pygame.Rect(self.x_offset, self.y_offset, 200, 300)
        self.button_dimensions = button_dimensions
        self.elements = {}
        self.elements_list = []
        self.selected_element = None
        self.scroll = 0
        # self.offset_x = offset_x

    def add_element(self, button_text, element_to_choose):

        game_button = MenuButton(button_text, self.new_element_top_left_corner_x, self.new_element_top_left_corner_y,
                                 self.button_dimensions, x_offset=self.x_offset, y_offset=self.y_offset, )
        game_button.draw(self.bottom_surf)

        self.upper_surf.blit(self.bottom_surf, (0, self.scroll))
        self.elements[game_button] = element_to_choose
        if not self.selected_element:
            self.selected_element = element_to_choose
        self.elements_list.append(game_button)
        self.new_element_top_left_corner_y += 40



    def check_scroll(self, y):
        mouse_pos = pygame.mouse.get_pos()
        if self.absolute_rect.collidepoint(mouse_pos):
            test_scroll = self.scroll + y * 10
            if test_scroll < 0 and test_scroll > - (self.bottom_surf.get_height() - self.upper_surf.get_height()):
                self.scroll = test_scroll
                self.upper_surf.fill(self.upper_surf_color)
                self.upper_surf.blit(self.bottom_surf, (0, self.scroll))
                [element.move_button(y * 10) for element in self.elements]

    def check_click(self, mouse_pos: tuple[int, int]):
        for element in self.elements:
            if element.check_click(mouse_pos):
                self.selected_element = self.elements[element]
                return self

    def draw(self, display_surface: pygame.Surface):
        if self.visible:
            display_surface.blit(self.upper_surf, (self.x_offset, self.y_offset))

# class ToggleButtonList(ButtonList):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.title_surface = pygame.Surface((200, 0))

class TextInput(UI_Element, TextObservable):
    def __init__(self, text=None, position=(10, 10), offset=(0, 0), editable=True, name=""):
        super().__init__(name=name)
        self.text = text
        self.position = position
        self.abs_position = (position[0] + offset[0], position[1] + offset[1])

        self.font = pygame.font.SysFont("Arial", 24)
        self.text_surf = self.font.render(self.text, True, '#FFFFFF')
        self.surf = pygame.Surface((200, 50))
        self.input_rect = pygame.Rect(10, 10, 180, 30)
        self.abs_rect = pygame.Rect(self.abs_position[0], self.abs_position[1], 200, 50)
        self.editable = editable
        self.active = False
        self.observers = []

    # def add_to_text(self):

    def draw(self, display_surface: pygame.Surface):
        if self.visible:
            self.surf = pygame.Surface((200, 50))
            pygame.draw.rect(self.surf, (0, 255, 0), self.input_rect, 2, 3)
            self.text_surf = self.font.render(self.text, True, '#FFFFFF')
            self.surf.blit(self.text_surf, (self.input_rect.x + 5, self.input_rect.y + 5))
            display_surface.blit(self.surf, self.position)

    def check_click(self, mouse_pos: tuple[int, int]):
        if self.abs_rect.collidepoint(mouse_pos):
            if self.editable:
                self.active = True
                print("notifying observers")
                self.notify_observers()
            return self

    def add_observer(self, observer):
        self.observers.append(observer)

    def remove_observer(self, observer):
        self.observers.remove(observer)

    def notify_observers(self, message=None):
        print("Observers in notify observers", self.observers)
        for observer in self.observers:
            if not message:
                observer.update(self)
            else:
                observer.update(message)
class Label(UI_Element):
    def __init__(self, text, position, name=""):
        super().__init__(name=name)
        self.text = text
        self.position = position
        self.font = pygame.font.SysFont("Arial", 24)
        self.text_surf = self.font.render(self.text, False,(0,255,0,) )

    def draw(self, display_surface: pygame.Surface):
        if self.visible:
            display_surface.blit(self.text_surf, self.position)
class ParametersSurface(UI_Element):
    def __init__(self, size: tuple[int, int], position: tuple[int, int], visible=True, name=""):
        super().__init__(name=name)
        self.visible = visible
        self.observers = []
        self.size = size
        self.surface = pygame.Surface(size, masks=(0, 0, 0))
        self.position = position
        self.rect = self.surface.get_rect(topleft=self.position)
        self.labels = {}
        self.add_lable("population", (10, 10), "population")
        self.add_lable("goods", (10, 30), "goods")
        self.add_lable("food", (10, 50), "food")

    def draw(self, display_surface: pygame.Surface):
        self.surface = pygame.Surface(self.size, masks=(0, 0, 0))
        for label in self.labels.values():
            label.draw(self.surface)
        display_surface.blit(self.surface, self.position)
    def add_lable(self,text, position, name):
        print("adding label", text, position, name)
        self.labels[name] = Label(str(text), position, name)
    def check_click(self, mouse_pos: tuple[int, int]):
        pass    
class UiSurface(UI_Element, TextObservable):
    def __init__(self, size: tuple[int, int], position: tuple[int, int], visible=False, name=""):

        super().__init__(name=name)
        self.visible = visible
        self.observers = []
        self.surface = pygame.Surface(size, masks=(0, 0, 0))
        self.position = position
        self.rect = self.surface.get_rect(topleft=self.position)
        self.elements = []
        # self.text_input = TextInput("tata", position=(10,10), offset=(500,0))
        # self.elements.append(self.text_input/)
        self.city = None
        self.generate_text_phields()

    def generate_text_phields(self):

        population = TextInput("", position=(10, 10), offset=self.position, name="population")
        cattle = TextInput("", position=(10, 60), offset=self.position, name="cattle")

        self.elements.append(population)
        self.elements.append(cattle)
        for observer in self.observers:
            self.add_observer(observer)

    def find_element(self, name):
        for element in self.elements:
            if element.name == name:
                return element

    def set_city(self, city):
        if self.city:
            try:
                self.city.population = int(self.find_element("population").text)
                self.city.cattle = self.find_element("cattle").text
            except Exception as e:
                print(e)

        self.city = city
        self.find_element("population").text = str(city.population)
        self.find_element("cattle").text = str(city.cattle)

    def hide(self):
        self.notify_observers(-1)
        self.visible = False
        for element in self.elements:
            element.visible = False

    def make_visible(self):
        self.visible = True
        for element in self.elements:
            element.visible = True

        # self

    def draw(self, display_surface: pygame.Surface):
        if self.visible:
            for element in self.elements:
                element.draw(self.surface)

            display_surface.blit(self.surface, self.position)

    def check_click(self, mouse_pos: tuple[int, int]):
        if self.rect.collidepoint(mouse_pos):
            self.notify_observers(-1)

            for element in self.elements:
                if element.check_click(mouse_pos):
                    return element
            return self

    def notify_observers(self, message=None):
        for observer in self.observers:
            if not message:
                observer.update(self)
            else:
                observer.update(message)

    def add_observer(self, observer):
        if not observer in self.observers:
            self.observers.append(observer)
        for element in self.elements:
            if isinstance(element, TextObservable):
                element.add_observer(observer)

    def remove_observer(self, observer):
        for element in self.elements:
            if isinstance(element, TextObservable):
                element.remove_observer(observer)
