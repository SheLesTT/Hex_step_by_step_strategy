import pygame

from player_actions.Buttons import ButtonForUnitSpawner,MenuButton
from player_actions.Spawner import Spawner
from main_components.Player import Player


class UI:
    def __init__(self, window_size, game_map, player):
        self.UI_surface = pygame.Surface(window_size, pygame.SRCALPHA)
        self.game_map = game_map
        self.spawner = Spawner(self.game_map,)
        print(self.spawner)
        self.buttons = self.add_buttons("Square")
        self.display_buttons(self.UI_surface)
        self.player = player



    def spawn_function(self, spawner,type,coords):
        spawner.spawn_unit(type, coords)
        string = "<spawn"+type+"("+str(coords[0])+","+str(coords[1])+")>"
        return string
    def end_turn(self, ):
        self.player.cur_turn = False
        self.player.moves = 0
        string = "<end_turn" + str(self.game_map.player_id) + ">"
        self.game_map.actions.add(string)
    def add_buttons(self, text):
        buttons = []
        titles = ["Triangular","Square","Circle"]
        display_size = pygame.display.get_surface().get_size()
        for i in range(len(titles)):
            button = ButtonForUnitSpawner(titles[i], display_size[0]-100, display_size[1]-100-100*i, 100, 100,
                                          self.spawner, action=self.spawn_function)
            buttons.append(button)
        finish_move = MenuButton("Finish Move", display_size[0]-100, display_size[1]-100-100*len(titles), 100, 100, self.end_turn,
                                                color=(255, 0, 0), font_size=24, font_name="Arial")
        buttons.append(finish_move)
        return buttons

    def display_buttons(self, surface):
        for button in self.buttons:
            button.draw(self.UI_surface)


    def fill_UI_surface(self):
        self.display_buttons(self.UI_surface)

    def check_click(self, game_map):
        for button in self.buttons:
            result = button.check_click()
            if result:
                return result
        return False

