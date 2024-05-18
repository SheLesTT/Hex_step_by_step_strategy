from abc import ABC, abstractmethod
import pygame, sys

from UI_staff.Interfaces import TextObservable, Scrollable
from UI_staff.UI import UI
from colors import Color as C


def empty_funciton():
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

    def check_click(self, mouse_pos: tuple[int, int]):
        pass
    def move_element(self, offset):
        pass


class Button(UI_Element):
    def __init__(self, text, x, y, button_dimensions: tuple[int, int], name="", x_offset=0, y_offset=0,
                 action=empty_funciton, color: tuple[int, int, int] = (0, 255, 0),
                 font_size: int = 24, font_name: str = "Arial", image=None):
        super().__init__(name=name)
        self.rect = pygame.Rect(x, y, button_dimensions[0], button_dimensions[1])

        self.text = text
        self.color = color
        self.action = action
        font = pygame.font.SysFont(font_name, font_size)
        self.text_surf = font.render(text, True, C.brown)
        self.text_rect = self.text_surf.get_rect(center=self.rect.center)
        self.image = image
        # self.is_clickable = False

    # def reset_clickability(self):
    #     self.is_clickable = True

    def draw(self, display_surface: pygame.Surface) -> None:
        if self.visible == True:
            if self.image:
                if isinstance(self.image, str):
                    self.image = pygame.image.load(self.image)
                display_surface.blit(self.image, self.rect)
            else:
                pygame.draw.rect(display_surface, self.color, self.rect)
                pygame.draw.rect(display_surface, "Black", self.rect, 2)
                display_surface.blit(self.text_surf, self.text_rect)

    @abstractmethod
    def check_click(self, pos) -> bool:
        pass


class MenuButton(Button):
    def __init__(self, text, x, y, button_dimensions: tuple[int, int], x_offset=0, y_offset=0,
                 action=empty_funciton, action_args=(),
                 color=(0, 255, 0), font_size=24, font_name="Arial", name="", image=None):
        super().__init__(text, x, y, button_dimensions, x_offset=x_offset, y_offset=y_offset, action=action,
                         color=color, font_size=font_size, font_name=font_name, name=name, image=image)
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

    def move_element(self, offset):
        self.y_offset += offset[1]
        self.abs_y += offset[1]
        self.absolute_rect = pygame.Rect(self.abs_x, self.abs_y, self.button_dimensions[0], self.button_dimensions[1])


class ButtonList(UI_Element, Scrollable):
    def __init__(self, bottom_surface_size: tuple[int, int] = (200, 400),
                 upper_surface_size: tuple[int, int] = (200, 200),
                 upper_surface_color: tuple[int, int, int] = C.brown,
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
                                 self.button_dimensions, color=C.yellow, x_offset=self.x_offset,
                                 y_offset=self.y_offset, )
        game_button.draw(self.bottom_surf)

        self.upper_surf.blit(self.bottom_surf, (0, self.scroll))
        self.elements[game_button] = element_to_choose
        if not self.selected_element:
            self.selected_element = element_to_choose
        self.elements_list.append(game_button)
        self.new_element_top_left_corner_y += 40

    def check_scroll(self, y):
        mouse_pos = pygame.mouse.get_pos()
        print("checking scroll")
        if self.absolute_rect.collidepoint(mouse_pos):
            print("collide")
            test_scroll = self.scroll + y * 10
            if test_scroll < 0 and test_scroll > - (self.bottom_surf.get_height() - self.upper_surf.get_height()):
                self.scroll = test_scroll
                self.upper_surf.fill(self.upper_surf_color)
                self.upper_surf.blit(self.bottom_surf, (0, self.scroll))
                [element.move_button(y * 10) for element in self.elements]
            return True

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
    def __init__(self, text=None, position=(10, 10), offset=(0, 0), size=(200, 50), bg_color=C.brown, editable=True,
                 name=""):
        super().__init__(name=name)
        self.text = text
        self.position = position
        self.size = size
        self.abs_position = (position[0] + offset[0], position[1] + offset[1])
        self.bg_color = bg_color
        self.font = pygame.font.SysFont("Arial", 24)
        self.text_surf = self.font.render(self.text, True, C.brown)
        self.surf = pygame.Surface(size)
        self.input_rect = pygame.Rect(10, 10, 180, 30)
        self.abs_rect = pygame.Rect(self.abs_position[0], self.abs_position[1], 200, 50)
        self.editable = editable
        self.active = False
        self.observers = []

    def move_element(self, offset):
        self.abs_position = (self.abs_position[0] + offset[0], self.abs_position[1] + offset[1])
        self.abs_rect = pygame.Rect(self.abs_position[0], self.abs_position[1], 200, 50)

    def draw(self, display_surface: pygame.Surface):
        if self.visible:
            self.surf = pygame.Surface((200, 50))
            self.surf.fill(C.yellow)
            pygame.draw.rect(self.surf, C.brown, self.input_rect, 2, 3, )
            self.text_surf = self.font.render(self.text, True, self.bg_color)
            self.surf.blit(self.text_surf, (self.input_rect.x + 5, self.input_rect.y + 5))
            display_surface.blit(self.surf, self.position)

    def change_color(self, color, display_surface: pygame.Surface):
        self.bg_color = color
        self.draw(display_surface)

    def check_click(self, mouse_pos: tuple[int, int]):
        if self.abs_rect.collidepoint(mouse_pos):
            print("TextInput was clicked")
            if self.editable:
                self.active = True
                self.notify_observers()
            return self

    def add_observer(self, observer):
        self.observers.append(observer)

    def remove_observer(self, observer):
        self.observers.remove(observer)

    def notify_observers(self, message=None):
        for observer in self.observers:
            if not message:
                observer.update(self)
            else:
                observer.update(message)


class Label(UI_Element):
    def __init__(self, text, position, name="", text_color=(0, 0, 0), visible=True):
        super().__init__(name=name)
        self.text = text
        self.position = position
        self.abs_position = position
        self.font = pygame.font.SysFont("Arial", 24)
        self.text_color = text_color
        self.text_surf = self.font.render(self.text, False, self.text_color)
    def change_text(self, text):
        self.text = text
        self.text_surf = self.font.render(self.text, False, self.text_color)

    def draw(self, display_surface: pygame.Surface):
        if self.visible:
            display_surface.blit(self.text_surf, self.position)





class TextBlock(UI_Element):
    pass

class UISurface(UI):

    def __init__(self, window_size, position, name=""):
        super().__init__(window_size)
        self.name = name
        self.position = position

    def draw(self, display_surface: pygame.Surface):
        for layer in self.elements:
            for element in layer:
                if element.visible:
                    element.draw(self.UI_surface)

        display_surface.blit(self.UI_surface, self.position)

class ExamSurface(UISurface, TextObservable):
    def __init__(self, size: tuple[int, int], position: tuple[int, int], visible=True, name=""):
        super().__init__(size, position, name=name)
        self.bottom_surf = pygame.Surface((size[0],size[1]+400), pygame.SRCALPHA)
        self.visible = visible
        self.observers = []
        self.size = size
        self.UI_surface = pygame.Surface(size, masks=(0, 0, 0))

        self.position = position
        self.absolute_rect = pygame.Rect(self.position[0], self.position[1], self.size[0], self.size[1])
        self.rect = self.UI_surface.get_rect(topleft=self.position)
        self.input_boxes = []
        self.answers = []
        self.scroll = 0

    def draw(self, display_surface: pygame.Surface):
        # self.UI_surface = pygame.Surface(self.size, masks=(0, 0, 0))
        # self.UI_surface.fill(C.yellow)
        super().draw(display_surface)


    def finish_test(self):
        for element, answer in zip(self.input_boxes, self.answers):
            if element.text == answer:
                position_for_lable = (
                element.position[0] + element.size[0] + 10, element.position[1] + element.size[1] // 2 - 10)
                self.add_label("correct", position_for_lable, "correct", color=C.brown)
                print("correct")
            else:
                position_for_lable = (
                element.position[0] + element.size[0] + 10, element.position[1] + element.size[1] // 2 - 10)
                self.add_label("wrong", position_for_lable, "wrong", color=C.brown)
                print("wrong")

    def add_label(self, text, position, name, color=(0, 0, 0)):
        self.add_element(0,Label(str(text), position, name, text_color=color))

    def build_surface(self, questions: list, answers: list):
        self.answers = answers
        font = pygame.font.SysFont("Arial", 24)
        y = 0
        for question_number, text in enumerate(questions):
            y = self.display_text(self.UI_surface, text, (0, y), font, (0, 255, 0))
            y += 10
            text_input = TextInput("", position=(10, y), offset=self.position, name="question" + str(question_number))
            self.add_element(0,text_input)
            self.input_boxes.append(text_input)
            y += 60

        finish_test = MenuButton("Finish test", 500, 500, button_dimensions=(200, 50),
                                 action=None, color=C.yellow, font_size=24, font_name="Arial",name = "finish_test")
        self.add_element(0,finish_test)



    def display_text(self, surface, text, pos, font, color):
        collection = [word.split(' ') for word in text.splitlines()]
        space = font.size(' ')[0]

        x, y = pos
        for line in collection:
            for word in line:
                word_surface = font.render(word, 0, color)
                word_width, word_height = word_surface.get_size()
                if x + word_width >= surface.get_width():
                    x = pos[0]  # Reset the x.
                    y += word_height  # Start on new row.
                surface.blit(word_surface, (x, y))
                x += word_width + space
            x = pos[0]  # Reset the x.
            y += word_height  # Start on new row.
        return y



    def notify_observers(self, message=None):
        for observer in self.observers:
            if not message:
                observer.update(self)
            else:
                observer.update(message)

    def add_observer(self, observer):
        if not observer in self.observers:
            self.observers.append(observer)
        for layer in self.elements:
            for element in layer:
                print(element, "checking element")
                if isinstance(element, TextObservable):
                    print(element.name, "observer added")
                    element.add_observer(observer)

    # def check_scroll(self, y):
    #     mouse_pos = pygame.mouse.get_pos()
    #     print("checking scroll")
    #     if self.absolute_rect.collidepoint(mouse_pos):
    #         print("collide")
    #         test_scroll = self.scroll + y * 10
    #         if test_scroll < 0 and test_scroll > - (self.bottom_surf.get_height() - self.UI_surface.get_height()):
    #             self.scroll = test_scroll
    #             self.UI_surface.fill(C.brown)
    #             self.UI_surface.blit(self.bottom_surf, (0, self.scroll))
    #             for layer in self.elements:
    #                 for element in layer:
    #                     element.move_element((0, y * 10))
    #         return True





class ParametersSurface(UISurface):
    def __init__(self, size: tuple[int, int], position: tuple[int, int], visible=True, name=""):
        super().__init__(window_size=size, position=position, name=name)
        self.visible = visible
        self.observers = []
        self.size = size
        self.UI_surface = pygame.Surface(size, masks=(0, 0, 0))
        self.UI_surface.fill(C.yellow)
        self.position = position
        self.rect = self.UI_surface.get_rect(topleft=self.position)
        self.init_labels()

    def init_labels(self):
        self.add_label("population", (10, 10), "population", color=C.brown)
        self.add_label("year", (10, 30), "year", color=C.brown)
        self.add_label("modeling speed", (10, 50), "modeling_speed", color=C.brown)

        self.add_label('', (150, 10), "population_val", color=C.brown)
        self.add_label('', (150, 30), "modeling_speed_val", color=C.brown)
        self.add_label('', (150, 50), "year_val", color=C.brown)

    def draw(self, display_surface: pygame.Surface):
        self.UI_surface = pygame.Surface(self.size, masks=(0, 0, 0))
        self.UI_surface.fill(C.yellow)
        super().draw(display_surface)

    def add_label(self, text, position, name, color=(0, 0, 0)):
        self.add_element(0, Label(str(text), position, name, color))



class UiSurface(UI_Element, TextObservable):
    def __init__(self, size: tuple[int, int], position: tuple[int, int], visible=False, name=""):

        super().__init__(name=name)
        self.visible = visible
        self.observers = []
        self.surface = pygame.Surface(size, masks=(0, 0, 0), )
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
        self.find_element("food").text = str(city.food)

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
