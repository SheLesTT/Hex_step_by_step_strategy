import math
import random
from abc import ABC
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


class MapObject(pygame.sprite.Sprite):
    def __init__(self, grid_pos):
        super().__init__()
        self.grid_pos = grid_pos
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
    def __init__(self, grid_pos, points_storage, color=(30, 70, 50), width=hex_width, height=hex_height):

        super().__init__(grid_pos)
        self.grid_pos = grid_pos
        self.points_storage = points_storage
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

        return str((self.grid_pos.row, self.grid_pos.column)), hex_dict

    def __repr__(self):
        return f"{self.__class__.__name__}"

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
    def __init__(self, grid_pos, game_map, color=(30, 70, 50), width=hex_width, height=hex_height):
        super().__init__(grid_pos, game_map, color, width=hex_width, height=hex_height)
        self.color = color
        self.type = "HexagonLand"
        self.draw()


class HexagonMountain(Hexagon):
    def __init__(self, grid_pos, game_map, color=(255, 255, 255), width=hex_width, height=hex_height):
        super().__init__(grid_pos, game_map, color, width=hex_width, height=hex_height)
        self.color = color
        self.type = "HexagonMountain"
        self.draw()


class HexagonSea(Hexagon):
    def __init__(self, grid_pos, game_map, color=(83, 236, 236), width=hex_width, height=hex_height):
        super().__init__(grid_pos, game_map, color, width=hex_width, height=hex_height)
        self.color = color
        self.type = "HexagonSea"
        self.draw()


class HexagonEmpty(Hexagon):
    def __init__(self, grid_pos, game_map, color=(0, 0, 0), width=hex_width, height=hex_height):
        super().__init__(grid_pos, game_map, color, width=hex_width, height=hex_height)
        self.color = color
        self.type = "HexagonEmpty"
        self.draw()


class Building(MapObject):
    def __init__(self, grid_pos):
        super().__init__(grid_pos)
        self.name = "building"
        self.population = 123
        self.food = 0
        self.goods = 0
        self.draw()
    def save_to_json(self):
        print("in buildings save to json")
        return {"name": str(self.name), "data": {"population": self.population, "cattle": self.cattle}}
    def draw(self):
        self.image = pygame.Surface((hex_width, hex_height), pygame.SRCALPHA)


    def visualise_parameter(self, parameter: str = None):
        print(f"visualising {parameter}, dict {self.__dict__}")
        self.draw()
        my_font = pygame.font.SysFont(str(self.__dict__[parameter]), 16)
        text_surface = my_font.render(str(self.__dict__[parameter]), False, (255, 255, 255))
        self.image.blit(text_surface, (0,19))

class Town(Building):
    def __init__(self, grid_pos):
        super().__init__(grid_pos)
        self.name = "Town"
        self.draw()

    def draw(self):
        super().draw()
        town_image = pygame.image.load("Resources/town.png")
        self.image.blit(town_image, (0, 0))


    def generate_parameters(self):
        self.population = random.randint(1000, 10000)
        self.goods = random.randint(50, 100)

    def produce(self):
        self.goods  = self.population * 0.1

    def consume(self):
        self.food -= self.population


class Village(Building):
    def __init__(self, grid_pos):
        super().__init__(grid_pos)
        self.name= "Village"
        self.draw()

    def draw(self):
        super().draw()
        village_image = pygame.image.load("Resources/village.png")
        print("drawing in village")
        self.image.blit(village_image, (0, 0))

    def generate_parameters(self):
        self.population = random.randint(25, 300)
        self.goods = random.randint(50, 100)
        self.food = random.randint(50, 100)

    def produce(self):
        self.food = self.population * 2

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
