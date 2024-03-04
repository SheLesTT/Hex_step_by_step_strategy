import pygame


class TextInputHandler:
    def __init__(self, user_interface):
        self.active_element = None
        self.user_interface = user_interface
        self.waiting_for_update = True

    def update(self, element):
        print("Updating text input handler")
        if element == -1 and self.waiting_for_update:
            self.remove_active_element()
        else:
            self.active_element = element

            self.waiting_for_update = False
        print(self.active_element)

    def remove_active_element(self):
        self.active_element = None

    def handle_input(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.waiting_for_update = True
        if self.active_element:
            if event.type == pygame.TEXTINPUT:
                self.active_element.text += event.text
                self.user_interface.draw_elements()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    self.active_element.text = self.active_element.text[:-1]
                    self.user_interface.draw_elements()