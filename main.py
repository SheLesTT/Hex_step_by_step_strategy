import yaml
from pygame.locals import *
import logging.config
from main_components.Map import Map
from main_components.MapEditorMouseClickHandler import MapEditorMouseClickHandler
from main_components.Render import Render
from main_components.TextInputHandler import TextInputHandler
from main_components.User_interface import EditorUI, SimUI
from main_components.mapMovement import MapMovementTracker
from player_actions.UI_Elements import *

from main_components.SimulationMouseClickHandler import SimulationMouseClickHandler

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.WARNING)
pygame.init()
clock = pygame.time.Clock()

window_size = (800, 800)
screen = pygame.display.set_mode(window_size)
internal_surface_size = (2500, 2500)
running = True


class Model:
    def __init__(self, game_map, user_interface, ):
        self.tracker = MapMovementTracker(internal_surface_size, window_size, )
        self.game_map = game_map
        self.user_interface = user_interface
        self.click_handler = MapEditorMouseClickHandler(self.game_map, self.user_interface, self.tracker)
        self.renderer = Render(internal_surface_size, map_movement_tracker=self.tracker,
                               user_interface=self.user_interface)
        self.text_input_handler = TextInputHandler(self.user_interface)

    def set_user_interface(self, UI):
        self.user_interface = UI

        self.tracker = MapMovementTracker(internal_surface_size, window_size, )
        self.renderer = Render(internal_surface_size, map_movement_tracker=self.tracker,
                               user_interface=self.user_interface)
        self.click_handler = SimulationMouseClickHandler(self.game_map, self.user_interface, self.tracker, )
        self.text_input_handler = TextInputHandler(self.user_interface)


def map_editor():
    run = True

    def stop_run():
        nonlocal run
        run = False

    game_map = Map(10, 10, id, 10, 3, True)
    user_interface = EditorUI(window_size, game_map)
    user_interface.find_element("exit").add_action(stop_run, ())
    model = Model(game_map, user_interface)
    model.user_interface.subscribe_text_elements(model.text_input_handler)

    def run_model(model, ):
        nonlocal run
        while run:
            print(run)

            events_list = pygame.event.get()
            model.game_map.hexes.update()
            model.renderer.display(events_list, model.game_map)
            pygame.display.flip()

            for event in events_list:
                if event.type == QUIT:
                    run = False
                    global running
                    running = False
                model.text_input_handler.handle_input(event)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    model.click_handler.handle_click(event)

            clock.tick(60)



    run_model(model)


def offline_game():
    run = True

    def stop_run():
        nonlocal run
        run = False

    game_map = Map(10, 10, id, 10, 3, True)
    user_interface = SimUI(window_size, game_map, )
    model = Model(game_map, user_interface)
    model.set_user_interface(user_interface)

    def run_model(model, ):
        nonlocal run
        while run:

            events_list = pygame.event.get()
            model.game_map.hexes.update()
            model.renderer.display(events_list, model.game_map)
            pygame.display.flip()

            for event in events_list:
                if event.type == QUIT:
                    run = False
                    global running
                    running = False
                model.text_input_handler.handle_input(event)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    model.click_handler.handle_click(event)

            clock.tick(60)



    run_model(model)


def game_menu():
    global running

    def stop_menue():
        global running
        running = False

    screen.fill((255, 255, 255))
    button_dimensions = (200, 50)
    offline_game_button = MenuButton("Start Simulation", 100, 100, button_dimensions=button_dimensions,
                                     action=offline_game, color=(0, 0, 255), font_size=24, font_name="Arial")

    exit_button = MenuButton("Exit", 100, 400, button_dimensions=button_dimensions,
                             action=stop_menue, color=(0, 0, 255), font_size=24, font_name="Arial")

    map_editor_button = MenuButton("Map Editor", 300, 100, button_dimensions=button_dimensions,
                                   action=map_editor, color=(0, 0, 255), font_size=24, font_name="Arial")

    buttons = [offline_game_button, exit_button, map_editor_button]

    for button in buttons:
        button.draw(screen)

    while running:
        print(running)



        if running:
            events_list = pygame.event.get()

            pygame.display.flip()
            for event in events_list:

                if event.type == QUIT:
                    running = False
                elif event.type == MOUSEBUTTONDOWN:
                    pos = event.dict["pos"]
                    [button.check_click(pos) for button in buttons]

            if not running:
                print("quitting")
                pygame.quit()
                sys.exit()


game_menu()
