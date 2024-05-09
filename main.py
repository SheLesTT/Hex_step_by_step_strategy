from threading import Thread
import time
from pygame.locals import *
import logging.config
from UI_staff.UI_surfaces.statisticsUI import StatisticsUI
from main_components.Map import Map
from main_components.MapEditorMouseClickHandler import MapEditorMouseClickHandler
from main_components.Render import Render
from UI_staff.TextInputHandler import TextInputHandler
from UI_staff.UI_surfaces.choose_sim_modelUI import ChooseSimModelUI
from UI_staff.UI_surfaces.simulationUI import SimUI
from UI_staff.UI_surfaces.edtiorUI import EditorUI
from UI_staff.UI_surfaces.choose_edit_modelUI import ChooseSavedModelUI
from main_components.mapMovement import MapMovementTracker
from UI_staff.UI_Elements import *

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
        self.renderer = Render(internal_surface_size, map_movement_tracker=self.tracker,
                               user_interface=self.user_interface)
        self.text_input_handler = TextInputHandler(self.user_interface)
        self.click_handler = None


def map_editor(file_to_load_from, rows=10, columns=10, new=False):
    run = True

    def stop_run():
        nonlocal run
        run = False

    game_map = Map(file_to_load_from, rows, columns, new)
    user_interface = EditorUI(window_size, game_map)
    user_interface.find_element("exit").add_action(stop_run, ())
    model = Model(game_map, user_interface)
    model.click_handler = MapEditorMouseClickHandler(model.game_map, model.user_interface, model.tracker)
    model.user_interface.subscribe_text_elements(model.text_input_handler)


    def run_model(model, ):
        nonlocal run
        while run:
            events_list = pygame.event.get()

            for event in events_list:
                if event.type == QUIT:
                    run = False
                    global running
                    running = False
                model.text_input_handler.handle_input(event)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    model.click_handler.handle_click(event)

                elif event.type == MOUSEWHEEL:
                    if user_interface.check_scroll(event.y):
                        events_list.remove(event)

            model.game_map.hexes.update()
            model.renderer.display(events_list, model.game_map)
            pygame.display.flip()

            clock.tick(60)


    # b.start()
    run_model(model)


def offline_game(filename):
    run = True

    def stop_run():
        nonlocal run
        run = False

    game_map = Map(filename)
    UI = SimUI(window_size, game_map, )
    model = Model(game_map, UI)
    model.click_handler = SimulationMouseClickHandler(model.game_map, model.user_interface, model.tracker)



    UI["exit"].add_action(stop_run)

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
                elif event.type == MOUSEWHEEL:
                    UI.check_scroll(event.y)

            clock.tick(10)

    # t.start()
    # time.sleep(1)

    # b.start()

    run_model(model)


def sim_model_loader():
    run = True

    UI = ChooseSimModelUI(window_size)

    def stop_menue():
        nonlocal run
        run = False

    screen.fill((255, 255, 255))

    def start_simulation():
        filename = UI["map_saves"].selected_element
        offline_game(filename)

    UI["exit"].add_action(stop_menue)
    UI["start_simulation"].add_action(start_simulation)

    while run:
        if run:
            events_list = pygame.event.get()

            screen.fill((255, 255, 255))
            screen.blit(UI.UI_surface, (0, 0))

            pygame.display.flip()
            for event in events_list:

                if event.type == QUIT:
                    run = False
                elif event.type == MOUSEBUTTONDOWN:
                    pos = event.dict["pos"]
                    UI.check_click(pos)
                elif event.type == MOUSEWHEEL:
                    UI.check_scroll(event.y)


def edit_model_loader():
    run = True

    UI = ChooseSavedModelUI(window_size)

    def stop_menue():
        nonlocal run
        run = False

    screen.fill((255, 255, 255))

    def start_editor():
        filename = UI["map_saves"].selected_element
        map_editor(filename)

    def create_new_map_for_editing():
        filename = UI["input_model_name"].text
        rows = UI["input_rows"].text
        columns = UI["input_columns"].text
        map_editor(filename, rows, columns, new=True)

    UI["exit"].add_action(stop_menue)
    UI["load_map"].add_action(start_editor)
    UI["start_simulation"].add_action(create_new_map_for_editing)

    text_handler = TextInputHandler(UI)
    UI.subscribe_text_elements(text_handler)

    while run:

        if run:
            events_list = pygame.event.get()

            screen.fill((255, 255, 255))
            screen.blit(UI.UI_surface, (0, 0))

            pygame.display.flip()
            for event in events_list:

                if event.type == QUIT:
                    run = False
                elif event.type == MOUSEBUTTONDOWN:
                    pos = event.dict["pos"]
                    UI.check_click(pos)
                elif event.type == MOUSEWHEEL:
                    UI.check_scroll(event.y)
                else:
                    text_handler.handle_input(event)
            UI.refresh_button_list()

            # if event.type == pygame.MOUSEWHEEL:
            #      map_saves.check_scroll(event.y)

def statistics():
    run = True

    UI =  StatisticsUI(window_size)

    def stop_menue():
        nonlocal run
        run = False

    screen.fill((255, 255, 255))


    UI["exit"].add_action(stop_menue)

    while run:

        if run:
            events_list = pygame.event.get()

            screen.fill((255, 255, 255))
            screen.blit(UI.UI_surface, (0, 0))

            pygame.display.flip()
            for event in events_list:

                if event.type == QUIT:
                    run = False
                elif event.type == MOUSEBUTTONDOWN:
                    pos = event.dict["pos"]
                    UI.check_click(pos)
                elif event.type == MOUSEWHEEL:
                    UI.check_scroll(event.y)

def game_menu():
    global running

    def stop_menue():
        global running
        running = False

    screen.fill((255, 255, 255))
    button_dimensions = (200, 50)
    offline_game_button = MenuButton("Start Simulation", 100, 100, button_dimensions=button_dimensions,
                                     action=sim_model_loader, color=(0, 0, 255), font_size=24, font_name="Arial")

    exit_button = MenuButton("Exit", 100, 400, button_dimensions=button_dimensions,
                             action=stop_menue, color=(0, 0, 255), font_size=24, font_name="Arial")

    map_editor_button = MenuButton("Map Editor", 300, 100, button_dimensions=button_dimensions,
                                   action=edit_model_loader, color=(0, 0, 255), font_size=24, font_name="Arial")
    statistics_button = MenuButton("Statistics", 300, 400, button_dimensions=button_dimensions,
                                   action=statistics, color=(0, 0, 255), font_size=24, font_name="Arial")
    buttons = [offline_game_button, exit_button, map_editor_button, statistics_button]

    for button in buttons:
        button.draw(screen)

    while running:

        if running:
            events_list = pygame.event.get()

            screen.fill((255, 255, 255))

            for button in buttons:
                button.draw(screen)
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
