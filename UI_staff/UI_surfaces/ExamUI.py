from UI_staff.UI import UI
from UI_staff.UI_Elements import MenuButton, ButtonList, ExamSurface, TextObservable
from colors import Color as C

class ExamUI(UI):
    def __init__(self, window_size):
        super().__init__(window_size)

        self.questions = [" 1) Какие социальные классы существовали в Средневековой Англии XIV века? \n"
"A) Король, дворяне, крестьяне, рабы \n"
"B) Король, дворяне, ремесленники, крестьяне\n"
"C) Король, феодалы, вассалы, крестьяне\n"
"D) Король, лорды, рыцари, крестьяне\n",
"2) Какой материал чаще всего использовался для строительства крестьянских жилищ в XIV веке?\n"
"A) Камень\n"
"B) Кирпич\n"
"C) Дерево и глина\n"
"D) Мрамор",
"Какие сельскохозяйственные культуры были основными в Англии XIV века?\n"
"A) Пшеница, ячмень, овес\n"
"B) Рис, кукуруза, картофель\n"
"C) Виноград, оливки, цитрусовые\n"
"D) Рожь, хлопок, сахарный тростник\n",
"Что входило в ежедневный рацион питания крестьян?\n"
"A) Мясо, вино, экзотические фрукты\n"
"B) Хлеб, овощи, немного мяса\n"
"C) Рыба, рис, тропические фрукты\n"
"D) Паста, оливковое масло, сыр\n",
"Как была организована система феодализма в Англии XIV века?\n"
"A) Крестьяне владели землей и платили налоги королю\n"
"B) Лорды предоставляли землю вассалам в обмен на военную службу\n"
"C) Король владел всей землей и сдавал её в аренду крестьянам\n"
"D) Вассалы управляли землей без обязательств перед лордами\n",
"Какие ремесла были наиболее развиты в средневековых английских городах?\n"
"A) Ювелирное дело, кузнечное дело, ткачество\n"
"B) Строительство кораблей, гончарное дело, резьба по дереву\n"
"C) Производство шелка, виноделие, хлебопечение\n"
"D) Литье стекла, производство бумаги, печатное дело\n"
]




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
        button_dimensions = (100,100)
        exit_button = MenuButton("Выход",  700, 0, button_dimensions=button_dimensions,
                                 action=None, color=C.yellow, font_size=24, font_name="Arial",name = "exit")

        self.add_element(0,exit_button)



    def init_questions_surface(self):
        questions_surface = ExamSurface((600, 1500), (100, 0), name="questions")
        questions_surface.build_surface(self.questions, answers=["D", "C", "A", "B","E","I"] )
        questions_surface["finish_test"].add_action(self.finish_test, ())
        questions_surface.add_update_observer(self)
        self.add_element(0, questions_surface)

    def subscribe_text_elements(self, observer, ):
        for layer in self.elements:
            for element in layer:
                if isinstance(element, TextObservable):
                    print(element.name, "observer added")
                    element.add_observer(observer)


