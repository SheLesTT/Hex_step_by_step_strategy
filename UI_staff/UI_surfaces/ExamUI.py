from UI_staff.UI import UI
from UI_staff.UI_Elements import MenuButton, ButtonList, ExamSurface, TextObservable
from colors import Color as C

class ExamUI(UI):
    def __init__(self, window_size):
        super().__init__(window_size)

        self.questions = ["Positioning of rotated surfaces is tricky. When drawing rotated text, the anchor point, the position you actually specify, remains fixed, and the text rotates around it. For instance, if you specify the top left of the text to be at (100, 100) with an angle of 90, then the Surface will actually be drawn so that its bottom left is at\n kdf \n cerjyl",
                          "this is my new text"]
        self.init_elements()
        self.draw_elements()

    def init_elements(self):
        self.init_questions_surface()
        self.init_buttons()
    def finish_test(self):
        self.find_element("questions").finish_test()
        self.draw_elements()




    def display_text(surface, text, pos, font, color):
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



    def init_buttons(self):
        button_dimensions = (200,50)
        exit_button = MenuButton("Exit",  600, 0, button_dimensions=button_dimensions,
                                 action=None, color=C.yellow, font_size=24, font_name="Arial",name = "exit")

        self.add_element(0,exit_button)



    def init_questions_surface(self):
        questions_surface = ExamSurface((600, 1200), (100, 100), name="questions")
        questions_surface.build_surface(self.questions, answers=["A", "B"] )
        questions_surface["finish_test"].add_action(self.finish_test, ())

        self.add_element(0, questions_surface)

    def subscribe_text_elements(self, observer, ):
        for layer in self.elements:
            for element in layer:
                if isinstance(element, TextObservable):
                    print(element.name, "observer added")
                    element.add_observer(observer)


