import math
import queue
import random
from abc import ABC
from dataclasses import dataclass
from math import cos, sin, pi, sqrt
from typing import NamedTuple

import pygame

from main_components.Errors import InvalidTriangleError

hex_side = 15 * sqrt(3)
hex_width = 30 * sqrt(3)
hex_height = hex_width / 2 * sqrt(3)


class OffsetCoordinates(NamedTuple):
    row: int
    column: int

    def __str__(self):
        return str((self.row, self.column))


class MapObject(pygame.sprite.Sprite):
    def __init__(self, grid_pos, game_map):
        super().__init__()
        self.grid_pos = grid_pos
        self.game_map = game_map
        self.width = 25
        self.height = 25
        self.name = "map object"
        self.surf = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.image = self.surf
        self.map_coords = self.calculate_coordinate_by_hex_position()
        self.rect = self.image.get_rect(center=self.map_coords)

    def __str__(self):
        return f"{self.name} {self.grid_pos[0]}, {self.grid_pos[1]}"

    def offset_to_cube_coords(self, grid_pos: OffsetCoordinates):
        q = grid_pos[0]
        r = grid_pos[1] - (grid_pos[0] - (grid_pos[0] & 1)) / 2
        return q, r, -q - r

    ## correct version. [col,row] in this order
    def offset_to_cube_coords_for_moving(self, grid_pos, offset):

        q = grid_pos[0]
        r = grid_pos[1] - (grid_pos[0] - offset * (grid_pos[0] & 1)) / 2
        return q, r, -q - r

    def calculate_coordinate_by_hex_position(self, ):
        map_coord_x = hex_width * (0.5 + 0.75 * self.grid_pos[0])

        if self.grid_pos[0] % 2 == 0:
            map_coord_y = hex_height * (0.5 + self.grid_pos[1])
        else:
            map_coord_y = hex_height * (1 + self.grid_pos[1])

        return map_coord_x, map_coord_y


class Hexagon(MapObject):
    def __init__(self, grid_pos, points_storage, game_map, color=(30, 70, 50), width=hex_width, height=hex_height):

        super().__init__(grid_pos, game_map)
        self.grid_pos = grid_pos
        self.points_storage = points_storage
        self.game_map = game_map
        self.color = color
        self.width = width
        self.height = height
        self.type = "hexagon"
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)  # Create a blank surface with transparency
        self.rect = self.image.get_rect(center=(self.map_coords[0], self.map_coords[1]))
        pygame.draw.polygon(self.image, self.color, self.points_storage.points)
        self.image.set_at(list(map(int, self.points_storage.points[0])), (225, 0, 0))
        self.mask = pygame.mask.from_surface(self.image)
        self.rivers = [False] * 6
        self.roads = [False] * 7
        self.directions = {0: pygame.Vector3(1, 0, -1), 1: pygame.Vector3(0, 1, -1), 2: pygame.Vector3(-1, 1, 0),
                           3: pygame.Vector3(-1, 0, 1), 4: pygame.Vector3(0, -1, 1), 5: pygame.Vector3(1, -1, -0)}
        self.village_territory = False

        self.neighbours = [None] * 6
        self.unit_on_hex = None
        self.building_on_hex = None

    def is_road_on_hex(self):
        return any(self.roads)

    def is_river_on_hex(self):
        return any(self.rivers)

    def save_to_json(self):
        hex_dict = {"type": str(self.__class__.__name__)}

        if self.building_on_hex:
            hex_dict["building_on_hex"] = self.building_on_hex.save_to_json()
        else:
            hex_dict["building_on_hex"] = None
        hex_dict["roads"] = self.roads
        hex_dict["rivers"] = self.rivers

        res = hex_dict
        return res

    def __repr__(self):
        return f"{self.type}, {self.grid_pos[0]}, {self.grid_pos[1]}"

    def add_unit(self, unit):
        self.unit_on_hex = unit

    def remove_unit(self):
        self.unit_on_hex = False

    def kill_unit(self):
        if self.unit_on_hex:
            self.unit_on_hex.hide_hexes()
            self.unit_on_hex.kill()
        self.remove_unit()

    def __str__(self):
        return f"{self.type}, {self.grid_pos[0]}, {self.grid_pos[1]}"

    def update(self):
        pass

    def draw(self):
        pygame.draw.polygon(self.image, self.color, self.points_storage.points)
        for idx, river in enumerate(self.rivers):
            if river:
                self.draw_a_river(idx)

        for idx, road in enumerate(self.roads):
            if road:
                self.draw_a_road(idx)

        if self.building_on_hex:
            self.building_on_hex.draw()
            self.image.blit(self.building_on_hex.image, (11, 4))

    def draw_a_river(self, triangle):
        pygame.draw.polygon(self.image, (0, 255, 255), self.points_storage.get_points_for_river(triangle))

    def draw_a_road(self, triangle_number):

        if triangle_number != 6:
            pygame.draw.polygon(self.image, (0, 30, 170), self.points_storage.get_points_for_road(triangle_number))
        elif triangle_number == 6 and not any(self.roads[:6]):

            pygame.draw.circle(self.image, (0, 30, 170), self.points_storage.get_points_for_road(triangle_number), 5)

    def add_building(self, building):
        self.building_on_hex = building
        self.discover_what_roads_to_draw()
        self.draw()

    def remove_building(self, ):
        self.building_on_hex = None
        self.remove_road()
        self.draw()

    def discover_rivers_to_draw(self, triangle):
        self.add_a_river(triangle)
        try:
            neigbour_hex = self.neighbours[triangle]

            opposite_triangle = (triangle + 3) % 6
            neigbour_hex.add_a_river(opposite_triangle)
        except IndexError as e:
            print("Invalid triangle number", triangle)

    def add_a_river(self, triangle):
        try:
            self.rivers[triangle] = True
        except IndexError as e:
            raise InvalidTriangleError()
        self.draw()

    def remove_river(self, triangle):
        self.rivers[triangle] = False
        self.draw()
        opposite_triangle = (triangle + 3) % 6
        if self.neighbours[triangle].rivers[opposite_triangle]:
            self.neighbours[triangle].remove_river(opposite_triangle)

    def discover_what_roads_to_draw(self, ):
        for direction, neighbour in enumerate(self.neighbours):
            if neighbour and any(neighbour.roads):
                neighbour.add_a_road((direction + 3) % 6)
                self.add_a_road(direction)
        if not any(self.roads):
            self.add_a_road(6)

    def add_a_road(self, triangle_number):
        try:
            self.roads[triangle_number] = True
            self.draw()
        except IndexError as e:
            raise InvalidTriangleError()

    def del_road(self, triangle):
        self.roads[triangle] = False
        if triangle != 6 and not any(self.roads[:6]):
            self.roads[6] = True

    def remove_road(self):
        for direction, neighbour in enumerate(self.neighbours):
            if self.roads[direction]:
                self.del_road(direction)
                opposite_triangle = (direction + 3) % 6
                print("ROads in a neigbour ", self.neighbours[direction])
                self.neighbours[direction].del_road(opposite_triangle)
                self.neighbours[direction].draw()
        self.del_road(6)
        self.draw()


class HexagonLand(Hexagon):
    def __init__(self, grid_pos, points_storage, game_map, color=(30, 70, 50), width=hex_width, height=hex_height):
        super().__init__(grid_pos, points_storage, game_map, color, width=hex_width, height=hex_height)
        self.color = color
        self.type = "HexagonLand"
        self.draw()


class HexagonMountain(Hexagon):
    def __init__(self, grid_pos, points_storage, game_map, color=(255, 255, 255), width=hex_width, height=hex_height):
        super().__init__(grid_pos, points_storage, game_map, color, width=hex_width, height=hex_height)
        self.color = color
        self.type = "HexagonMountain"
        self.draw()


class HexagonSea(Hexagon):
    def __init__(self, grid_pos, points_storage, game_map, color=(83, 236, 236), width=hex_width, height=hex_height):
        super().__init__(grid_pos, points_storage, game_map, color, width=hex_width, height=hex_height)
        self.color = color
        self.type = "HexagonSea"
        self.draw()


class HexagonEmpty(Hexagon):
    def __init__(self, grid_pos, points_storage, game_map, color=(0, 0, 0), width=hex_width, height=hex_height):
        super().__init__(grid_pos, points_storage, game_map, color, width=hex_width, height=hex_height)
        self.color = color
        self.type = "HexagonEmpty"
        self.draw()


class HexagonForest(HexagonLand):
    def __init__(self, grid_pos, points_storage, game_map, color=(30, 70, 50), width=hex_width, height=hex_height):
        super().__init__(grid_pos, points_storage, game_map, color, width=hex_width, height=hex_height)
        self.color = color
        self.type = "HexagonForest"
        self.draw()

    def draw(self):
        super().draw()
        forest_image = pygame.image.load("Resources/forest.png")
        self.image.blit(forest_image, (9, 5))


class HexagonWheat(Hexagon):
    def __init__(self, grid_pos, points_storage, game_map, fertility, mod, color=(30, 70, 50), ):
        self.fertility_colors = {"maximum": (76, 183, 27), "medium": (130, 203, 69), "low": (199, 134, 70),
                                 "minimum": (135, 147, 1)}
        super().__init__(grid_pos, points_storage, game_map, color, width=hex_width, height=hex_height)
        self.color = color
        self.type = "HexagonWheat"
        if fertility:
            self.fertility = float(fertility)

        else:
            self.fertility = self.create_fertility()
        self.mods_list = {'wheat': "Resources/wheat.png", 'barley': "Resources/grape.png",
                          'rest': "Resources/sheep.png"}
        self.mods = queue.Queue()
        [self.mods.put(mod) for mod in self.mods_list.keys()]
        if mod:
            self.current_mod = None
            self.change_mod(mod)
        else:
            self.current_mod = 'wheat'
        self.check_fertility()
        self.draw()
        self.producing = True

    def draw(self, ):
        super().draw()
        forest_image = pygame.image.load(self.mods_list[self.current_mod])
        self.image.blit(forest_image, (9, 5))

    def create_fertility(self):
        return random.uniform(0.5, 1)

    def change_mod(self, culture=''):
        if culture in self.mods_list.keys():
            while self.current_mod != culture:
                self.current_mod = self.mods.get()
                self.mods.put(self.current_mod)
        else:
            self.current_mod = self.mods.get()
            self.mods.put(self.current_mod)
        self.draw()

    def produce(self, modifier=1) -> dict:
        production = None
        if self.current_mod == 'rest':
            production = {}
        if self.current_mod == 'wheat':
            production = 1000 * modifier * self.fertility
            production = {'wheat':production}
        if self.current_mod == 'barley':
            production = 1000 * modifier * self.fertility
            production = {'barley':production}
        self.change_fertility()
        self.check_fertility()
        self.change_mod()
        return production

    def change_fertility(self, modifier=1):
        if self.current_mod != 'rest':
            if self.fertility > 0:
                self.fertility -= 0.1
        else:
            self.fertility += 0.2

    def stop_producing(self):
        self.producing = False

    def start_producing(self):
        self.producing = True

    def check_fertility(self):
        new_color = self.color
        if 0.80 < self.fertility <= 1:
            new_color = self.fertility_colors["maximum"]
        elif 0.55 < self.fertility <= 0.80:
            new_color = self.fertility_colors["medium"]
        elif 0.20 < self.fertility <= 0.55:
            new_color = self.fertility_colors["low"]
        elif 0 <= self.fertility <= 0.20:
            new_color = self.fertility_colors["minimum"]
        if new_color != self.color:
            self.color = new_color

            self.draw()

    def save_to_json(self):
        save_dict = super().save_to_json()
        save_dict.update({'fertility': str(self.fertility), 'mod':self.current_mod})
        return save_dict


class HexagonSheep(HexagonLand):
    def __init__(self, grid_pos, points_storage, game_map, color=(30, 70, 50), width=hex_width, height=hex_height):
        super().__init__(grid_pos, points_storage, game_map, color, width=hex_width, height=hex_height)
        self.color = color
        self.type = "HexagonSheep"
        self.draw()

    def draw(self):
        super().draw()
        forest_image = pygame.image.load("Resources/sheep.png")
        self.image.blit(forest_image, (9, 5))


class HexagonGrape(HexagonLand):
    def __init__(self, grid_pos, points_storage, game_map, color=(30, 70, 50), width=hex_width, height=hex_height):
        super().__init__(grid_pos, points_storage, game_map, color, width=hex_width, height=hex_height)
        self.color = color
        self.type = "HexagonGrape"
        self.draw()

    def draw(self):
        super().draw()
        forest_image = pygame.image.load("Resources/grape.png")
        self.image.blit(forest_image, (9, 5))


class Building(MapObject):
    def __init__(self, grid_pos, game_map):
        super().__init__(grid_pos, game_map)
        self.name = "building"
        self.population = 123
        self.food = 0
        self.goods = 0
        self.parameter_for_visualisation = None
        self.storage = ProductionStorage(sheep=0, pigs=0, wheat=0, barley=0)
        self.draw()
        self.statistics = {"population": [], "food": [], "goods": []}

    def save_to_json(self):
        return {"name": str(self.name), "data": {"population": self.population, "food": self.food, "goods": self.goods}}

    def draw(self):
        self.image = pygame.Surface((hex_width, hex_height), pygame.SRCALPHA)

    def get_parameter(self, parameter: str):
        return self.__dict__[parameter]

    def draw_parameter_for_visualisation(self):
        if self.parameter_for_visualisation:
            parameter = self.get_parameter(self.parameter_for_visualisation)
            my_font = pygame.font.SysFont(str(parameter), 16)
            text_surface = my_font.render(str(parameter), False, (255, 255, 255))
            self.image.blit(text_surface, (0, 19))

    def collect_statistics(self):
        self.statistics["population"].append(self.population)
        for key, value in self.storage.__dict__.items():
            if self.statistics.get(key):
                self.statistics[key].append(value)
            else:
                self.statistics[key] = [value]

    def yearly_calculation(self, pandemic_severity):
        self.produce()
        try:
            self.storage.consume_production({'wheat': self.population *40, 'barley': self.population * 10})
        except ValueError as e:
            self.population -=10
        self.population = int(
            self.population - self.population * (0.5 * pandemic_severity * random.triangular(0.8, 0.9, 1.1)))
        self.population += 5
        self.collect_statistics()
    def produce(self):
        print("produce")
        pass
    def change_visualization_parameter(self, parameter: str):
        self.parameter_for_visualisation = parameter
        self.draw()


class Town(Building):
    def __init__(self, grid_pos, game_map):
        super().__init__(grid_pos, game_map)
        self.name = "Town"
        self.draw()

    def draw(self):
        super().draw()
        town_image = pygame.image.load("Resources/town.png")
        self.image.blit(town_image, (0, 0))
        self.draw_parameter_for_visualisation()

    def generate_parameters(self):
        self.population = random.randint(1000, 10000)
        self.goods = random.randint(50, 100)

    def produce(self):
        self.goods = self.population * 0.1

    def consume(self):
        self.food -= self.population


# class VillageTileManager:
#     def __init__(self, territories):
@dataclass
class ProductionStorage:
    sheep: int
    pigs: int
    wheat: int
    barley: int
    def __getitem__(self, item):
        return self.__dict__.get(item)
    def __setitem__(self, key, value):
        self.__dict__[key] = value
    def add_production(self, production:dict):

        for key, value in production.items():
            if self[key]:
                self[key] += int (value)
            else:
                self[key] = int(value)
    def consume_production(self, production:dict):
        for key, value in production.items():
            if self[key] and self[key] >= int(value):
                self[key] -= int(value)
            else:
                raise ValueError(f"Insufficient {key} production")


class TerritoryHandler:
    def __init__(self, territories):
        self.available_territories = territories
        self.territories = []
        self.wheat_mods = ('wheat', 'barley', 'rest')
        self.next_mod = queue.Queue()
        [self.next_mod.put(mod) for mod in self.wheat_mods]

    def append(self, hex: Hexagon):
        if isinstance(hex, HexagonWheat):
            mod = self.next_mod.get()
            self.next_mod.put(mod)
            hex.change_mod(mod)
        self.territories.append(hex)

    def get_free_hex(self) -> Hexagon | None:
        print(self.available_territories)
        if self.available_territories:
            hex_to_change = random.choice(self.available_territories)
            self.available_territories.remove(hex_to_change)
            return hex_to_change
        return None
    def produce(self):
        production = ProductionStorage(sheep=0, pigs=0, wheat=0, barley=0)
        for hexagon in self.territories:
            if isinstance(hexagon, HexagonWheat):
                result_prod = hexagon.produce()
                production.add_production(result_prod)
        return production.__dict__


class Village(Building):
    def __init__(self, grid_pos, game_map, loading=False):
        super().__init__(grid_pos, game_map)
        self.name = "Village"
        self.population = 100
        self.forest_area = 99
        self.pastures_area = 99
        self.storage = ProductionStorage(sheep=0, pigs=0, wheat=0, barley=0)
        self.generate_parameters()
        self.draw()
        self.controlled_territories = []
        self.territory_handler = None
        if not loading:
            self.initialize()
            self.create_initial_territories()

    def generate_parameters(self):
        self.population = random.randint(50, 360)
        self.forest_area = random.randint(25, 149)
        self.pastures_area = random.randint(25, 149)

    def initialize(self):
        hexes_in_range = self.game_map.coordinate_range(self.game_map.hexes[self.grid_pos], 2)
        self.territory_handler = TerritoryHandler(hexes_in_range)
    def save_to_json(self):
        save_dict = super().save_to_json()
        save_dict['data']['territories'] = [hex.grid_pos for hex in self.territory_handler.territories]
        return save_dict


    def draw(self):
        super().draw()
        village_image = pygame.image.load("Resources/village.png")
        self.image.blit(village_image, (0, 0))
        self.draw_parameter_for_visualisation()

    def create_initial_territories(self):
        print("in create initial territories")
        crops_phields = max(12, min(3, math.ceil(self.population / 30)))
        for i in range(crops_phields):
            hex_to_change = self.territory_handler.get_free_hex()
            hex_created = self.game_map.change_hex("HexagonWheat", hex_to_change.grid_pos)
            self.territory_handler.append(hex_created)
        forests = math.ceil(self.forest_area / 50)
        pastures = math.ceil(self.pastures_area / 50)
        for i in range(forests):
            hex_to_change = self.territory_handler.get_free_hex()
            hex_created = self.game_map.change_hex("HexagonForest", hex_to_change.grid_pos)
            self.territory_handler.append(hex_created)
        for i in range(pastures):
            hex_to_change = self.territory_handler.get_free_hex()
            hex_created = self.game_map.change_hex("HexagonSheep", hex_to_change.grid_pos)
            self.territory_handler.append(hex_created)

    def produce(self):
        self.storage.add_production(self.territory_handler.produce())
        print(self.storage)

    def consume(self):
        self.food -= self.population


class Mine(Building):
    def __init__(self, grid_pos):
        super().__init__(grid_pos)
        self.draw()

    def draw(self):
        super().draw()
        coin_image = pygame.image.load("Resources/goldcoin1.png")
        self.image.blit(coin_image, (-17, -20))
