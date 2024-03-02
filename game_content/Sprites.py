import math
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

        self.neighbours = None
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

        return str(self.grid_pos), hex_dict

    def __repr__(self):
        return f"{self.__class__.__name__}, {self.unit_on_hex}, {self.building_on_hex}"



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

        if triangle_number == 6:
            pygame.draw.circle(self.image, (0, 30, 170), self.points_storage.get_points_for_road(triangle_number), 5)
        else:
            self.roads[6] = False
            pygame.draw.polygon(self.image, (0, 30, 170), self.points_storage.get_points_for_road(triangle_number))



    def add_building(self, building):
        self.building_on_hex = building
        self.draw()

    def discover_rivers_to_draw(self, triangle):
        self.add_a_river(triangle)
        neigbour_hex = self.neighbours[triangle]
        new_triangle = (triangle + 3) % 6
        neigbour_hex.add_a_river(new_triangle)

    def add_a_river(self, triangle):
        try:
            self.rivers[triangle] = True
        except IndexError as e:
            raise InvalidTriangleError()
        self.draw()


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



class HexagonLand(Hexagon):
    def __init__(self, grid_pos, game_map, color=(30, 70, 50), width=hex_width, height=hex_height):
        super().__init__(grid_pos, game_map, color, width=hex_width, height=hex_height)
        self.color = color
        self.type = "land Hexagon"
        self.draw()


class HexagonMountain(Hexagon):
    def __init__(self, grid_pos, game_map, color=(255, 255, 255), width=hex_width, height=hex_height):
        super().__init__(grid_pos, game_map, color, width=hex_width, height=hex_height)
        self.color = color
        self.type = "mountain Hexagon"
        self.draw()


class HexagonSea(Hexagon):
    def __init__(self, grid_pos, game_map, color=(83, 236, 236), width=hex_width, height=hex_height):
        super().__init__(grid_pos, game_map, color, width=hex_width, height=hex_height)
        self.color = color
        self.type = "sea Hexagon"
        self.draw()


class HexagonEmpty(Hexagon):
    def __init__(self, grid_pos, game_map, color=(0, 0, 0), width=hex_width, height=hex_height):
        super().__init__(grid_pos, game_map, color, width=hex_width, height=hex_height)
        self.color = color
        self.type = "empty Hexagon"
        self.draw()


class Building(MapObject):
    def __init__(self, grid_pos):
        super().__init__(grid_pos)
        self.image = pygame.Surface((hex_width, hex_height), pygame.SRCALPHA)
        self.name = "building"
        self.population = 123
        self.cattle = 0

    def save_to_json(self):
        print("in buildings save to json")
        return {"name": str(self.__class__.__name__), "data": {"population": self.population, "cattle": self.cattle}}


class Town(Building):
    def __init__(self, grid_pos):
        super().__init__(grid_pos)
        type = "town"
        town_image = pygame.image.load("Resources/town.png")
        self.image.blit(town_image, (0, 0))


class Village(Building):
    def __init__(self, grid_pos):
        super().__init__(grid_pos)
        type = "village"
        village_image = pygame.image.load("Resources/village.png")
        self.image.blit(village_image, (0, 0))


class Mine(Building):
    def __init__(self, grid_pos):
        super().__init__(grid_pos)
        coin_image = pygame.image.load("Resources/goldcoin1.png")
        self.image.blit(coin_image, (-17, -20))
