import json
from collections import deque, defaultdict

import pygame

from math import *

from game_content.Groups import HexesGroup
from game_content.Sprites import Hexagon, HexagonMountain, HexagonSea, HexagonLand, Town, HexagonEmpty
from game_content.sprites_factory import HexesFactory
from player_actions.Spawner import Spawner
from noise.Noise import Noise
import random


class Map:

    def __init__(self, rows, columns, player_id, seed, players_amount=2, Offline=False):
        self.seed = seed
        random.seed(self.seed)

        self.rows = rows
        self.columns = columns
        self.hexes_factory = HexesFactory()

        self.hex_width = 30 * sqrt(3)
        # self.hexes   = self.create_tiles()

        # self.hexes = self.load_from_json("json_save")
        self.hexes = self.create_empty_map()
        self.find_neighbours()
        self.Spawner = Spawner(self)
        # self.create_mines()

        # self.spawner = Spawner(self)

    def create_graph(self):
        queue = deque()
        graph = defaultdict(list)
        visited = [[False for _ in range(self.columns)] for _ in range(self.rows)]
        previous = [[None for _ in range(self.columns)] for _ in range(self.rows)]
        for hex in self.hexes:
            if hex.building_on_hex and not visited[hex.grid_pos[0]][hex.grid_pos[1]]:
                visited[hex.grid_pos[0]][hex.grid_pos[1]] = True
                queue.append(hex)

                while queue:
                    cur_hex = queue.popleft()
                    if cur_hex.building_on_hex:
                        print("found a city", cur_hex.grid_pos)
                        prev_hex = self.hexes[previous[cur_hex.grid_pos[0]][cur_hex.grid_pos[1]]]
                        count = 0
                        if prev_hex:
                            while not prev_hex.building_on_hex:
                                count += 1
                                prev_hex = self.hexes[previous[prev_hex.grid_pos[0]][prev_hex.grid_pos[1]]]
                            graph[prev_hex.grid_pos].append((cur_hex.grid_pos, count))
                            graph[cur_hex.grid_pos].append((prev_hex.grid_pos, count))



                    for neighbour in cur_hex.get_neighbours():
                        if neighbour.is_road_on_hex() and not visited[neighbour.grid_pos[0]][neighbour.grid_pos[1]]:
                            visited[neighbour.grid_pos[0]][neighbour.grid_pos[1]] = True
                            previous[neighbour.grid_pos[0]][neighbour.grid_pos[1]] = cur_hex.grid_pos
                            queue.append(neighbour)

        print(graph)



    def load_from_json(self, name: str) -> HexesGroup:
        hexes = HexesGroup()

        with open(name, "r") as f:
            hexes_json = json.load(f)

        for grid_pos, hex_params in hexes_json.items():
            grid_pos = tuple(map(int, grid_pos[1:-1].split(",")))

            hex_created = self.create_hex(hex_params["type"], grid_pos)
            hex_created.draw()
            hexes.add(hex_created)
        return hexes

    def save_to_json(self, file_name):

        map_dict = {}
        for hex in self.hexes:
            grid_pos, d = hex.save_to_json()
            map_dict[grid_pos] = d
        with open(file_name, "w") as f:
            json.dump(map_dict, f)



    def create_hex(self, type:str, grid_pos: tuple[int, int]) -> Hexagon:
        hex_created = self.hexes_factory.create_hex(type, grid_pos)
        return hex_created

    def change_hex(self, type, grid_pos):
        old_hex = self.hexes[grid_pos]
        hex_created = self.hexes_factory.replace_hex(type, grid_pos, old_hex)

        self.hexes[grid_pos] = hex_created

    def find_neighbours(self,):
        for hex in self.hexes:
            coords = hex.offset_to_cube_coords(hex.grid_pos)
            hex.neighbours = list(filter(None, [self.hexes[tuple(coords + direction)] for direction in hex.directions.values()]))



    def get_hex_by_coord(self, grid_pos):
        if grid_pos[0] in range(0, self.columns + 1) and grid_pos[0] in range(0, self.rows + 1):
            return self.hexes[grid_pos]
        return False

    def get_cube_coords(self, hex):
        return self.hexes.get_hex_cube_coords(hex)

    def calculate_distance(self, hex1, hex2):

        cube_coords1 = self.get_cube_coords(hex1)
        cube_coords2 = self.get_cube_coords(hex2)

        return int((abs(cube_coords1[0] - cube_coords2[0]) + abs(cube_coords1[1] - cube_coords2[1]) + abs(
            cube_coords1[2] - cube_coords2[2])) // 2)


    def create_tiles(self):
        noise = Noise(self.rows, self.columns, seed=self.seed)
        hexes = noise.create_tiles()
        return hexes
    def create_empty_map(self):
        hexes = HexesGroup()
        for i in range(self.rows):
            for j in range(self.columns):

                hexes.add(self.hexes_factory.create_hex("HexagonEmpty", (i, j)))
        return hexes


    def check_coord_validity(self, cords):
        return cords[0] >= 0 and cords[1] >= 0 and cords[0] < self.rows and cords[1] < self.columns

    def coordinate_range(self, hex, distance):
        hexes = []
        distance = int(distance)
        qs, rs, ss = map(int, self.get_cube_coords(hex))
        for q in range(qs - distance, qs + distance + 1):

            for r in range(rs - distance, rs + distance + 1):
                for s in range(ss - distance, ss + distance + 1):

                    if q + r + s == 0 and q >= 0 and q < self.columns and r > -self.rows and s <= 0:

                        hex = self.hexes[(q, r, s)]
                        if hex:
                            hexes.append(hex)
        return hexes

    def __str__(self):
        return f"map with {self.rows} rows and {self.columns} columns"


