import json
from collections import deque, defaultdict
from heapq import *
from typing import List

import pygame

from math import *

from UI_staff.Interfaces import Observable
from game_content.Groups import HexesGroup
from game_content.Sprites import Hexagon, HexagonMountain, HexagonSea, HexagonLand, Town, HexagonEmpty, \
    OffsetCoordinates, Village, Building
from game_content.sprites_factory import HexesFactory

class GlobalParameters(Observable):

    def __init__(self):
        super().__init__()
        self.observers = []
        self.population = 0
        self.food = 0
        self.goods = 0
        self.year = 1200
        self.modeling_speed = 1

    def add_observer(self, observer):
        if not observer in self.observers:
            self.observers.append(observer)
    def notify_observers(self, parameter=None, value=None):
        for observer in self.observers:
            observer.update(parameter,value)
    def change_parameter(self, parameter, value):
        self.__dict__[parameter] = value
        self.notify_observers(parameter,value)

class Map:

    def __init__(self, file_to_load_from, rows=10, columns=10, new=False):

        self.rows = int(rows)
        self.columns = int(columns)
        self.file_to_load_from = file_to_load_from
        self.hexes_factory = HexesFactory(self)
        self.new = new
        self.hex_width = 30 * sqrt(3)
        self.buildings = []
        self.statistics = {"population": [], "food": [], "goods": []}
        # self.hexes   = self.create_tiles()

        if self.new:
             self.create_empty_map()
        else:
            self.load_from_json(self.file_to_load_from)
        self.find_neighbours()
        self.global_parameters = GlobalParameters()
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
                        prev_hex = self.hexes[previous[cur_hex.grid_pos[0]][cur_hex.grid_pos[1]]]
                        count = 0
                        if prev_hex:
                            while not prev_hex.building_on_hex:
                                count += 1
                                prev_hex = self.hexes[previous[prev_hex.grid_pos[0]][prev_hex.grid_pos[1]]]
                            graph[prev_hex.building_on_hex].append((count, cur_hex.building_on_hex))
                            graph[cur_hex.building_on_hex].append((count,  prev_hex.building_on_hex ))

                    for neighbour in cur_hex.neighbours:
                        if neighbour.is_road_on_hex() and not visited[neighbour.grid_pos[0]][neighbour.grid_pos[1]]:
                            visited[neighbour.grid_pos[0]][neighbour.grid_pos[1]] = True
                            previous[neighbour.grid_pos[0]][neighbour.grid_pos[1]] = cur_hex.grid_pos
                            queue.append(neighbour)
        print(graph)
        return graph

    def find_nearest_town(self,graph: dict, start: Building,) -> Town | None:

        nearest_town = (float('inf'), None)
        queue = []
        heappush(queue, (0, start))
        cost_visited = {start: 0}
        visited = {start: None}

        while queue:
            print(queue)
            current_cost, current = heappop(queue)
            print("this is cost", current_cost, current)
            if isinstance(current, Town) and current_cost < nearest_town[0]:
                nearest_town = (current_cost, current)
            for next_cost, next in graph[current]:
                new_cost = current_cost + next_cost
                if (next not in cost_visited or new_cost < cost_visited[next]) and new_cost < nearest_town[0]:
                    cost_visited[next] = new_cost
                    heappush(queue, ( new_cost, next))
                    visited[next] = current
        if nearest_town[1] is None:
            return None
        return nearest_town

    def calculate(self):
        i = 1
        while i < 100:
            i+=1
            for city, neighbours in self.graph.items():
                neighbours = [neighbour[0] for neighbour in neighbours]
                for neighbour in neighbours:
                    if city.population < neighbour.population:
                        city.population += 1
                        neighbour.population -= 1


    def load_from_json(self, name: str) -> HexesGroup:
        hexes = HexesGroup()
        with open("./model_saves/" + name, "r") as f:
            map_json= json.load(f)
            meta_json =map_json["meta_info"]
            self.rows = int(meta_json["rows"])
            self.columns = int(meta_json["columns"])
            hexes_json = map_json["map"]
        for grid_pos, hex_params in hexes_json.items():
            grid_pos = OffsetCoordinates(*list(map(int, grid_pos[1:-1].split(","))))
            hex_created = self.create_hex(hex_params, grid_pos, loading=True)
            hex_created.draw()
            hexes.add(hex_created)
            if hex_created.building_on_hex:
                self.buildings.append(hex_created)
        self.hexes = hexes
        for building in self.buildings:
            build = building.building_on_hex
            if isinstance(build, Village):
                build.initialize()
                territories = [self.hexes[tuple(grid_pos)]  for grid_pos in hexes_json[str(building.grid_pos)]['building_on_hex']["data"]["territories"] ]
                build.territory_handler.territories = territories



    def save_to_json(self, ):

        map_dict = {}
        for hex in self.hexes:
            d = hex.save_to_json()
            map_dict[str(hex.grid_pos)] = d
        final_dict = {"meta_info":{"rows":self.rows, "columns" :self.columns}, "map": map_dict}
        with open("./model_saves/" + self.file_to_load_from, "w") as f:
            json.dump(final_dict, f, sort_keys=True, indent=4)

    def create_hex(self, hex_params: dict, grid_pos: OffsetCoordinates, loading=False) -> Hexagon:
        hex_created = self.hexes_factory.create_hex(hex_params, grid_pos,loading=loading)
        return hex_created

    def set_hex(self, hexagon):
        self.hexes[hexagon.grid_pos] = hexagon

    def change_hex(self, hex_type: str, grid_pos: OffsetCoordinates) -> None:
        old_hex = self.hexes[grid_pos]
        hex_created = self.hexes_factory.replace_hex(hex_type, grid_pos, old_hex)

        self.hexes[grid_pos] = hex_created
        return hex_created

    def find_neighbours(self, ):
        for hex in self.hexes:
            coords = hex.offset_to_cube_coords(hex.grid_pos)
            hex.neighbours = list(
                filter(None, [self.hexes[tuple(coords + direction)] for direction in hex.directions.values()]))

    def get_hex_by_coord(self, grid_pos: OffsetCoordinates):
        if grid_pos.column in range(0, self.columns + 1) and grid_pos.row in range(0, self.rows + 1):
            return self.hexes[grid_pos]
        return False

    def get_cube_coords(self, hex):
        return self.hexes.get_hex_cube_coords(hex)

    def calculate_distance(self, hex1, hex2):

        cube_coords1 = self.get_cube_coords(hex1)
        cube_coords2 = self.get_cube_coords(hex2)

        return int((abs(cube_coords1[0] - cube_coords2[0]) + abs(cube_coords1[1] - cube_coords2[1]) + abs(
            cube_coords1[2] - cube_coords2[2])) // 2)


    def create_empty_map(self):
        hexes = HexesGroup()
        for i in range(self.rows):
            for j in range(self.columns):
                hexes.add(self.hexes_factory.create_hex({'type':"HexagonLand"}, OffsetCoordinates(i, j),))
        self.hexes = hexes
    def check_coord_validity(self, cords: OffsetCoordinates):
        return 0 <= cords.row < self.rows and 0 <= cords.column < self.columns

    def coordinate_range(self, hex: Hexagon, distance: int) -> List[Hexagon]:
        hexes = []
        distance = int(distance)
        qs, rs, ss = map(int, self.get_cube_coords(hex))
        for q in range(qs - distance, qs + distance + 1):

            for r in range(rs - distance, rs + distance + 1):
                for s in range(ss - distance, ss + distance + 1):

                    if q + r + s == 0 and q >= 0 and q < self.columns and r > -self.rows and s <= 0:

                        hex_new = self.hexes[(q, r, s)]
                        if hex_new and hex.grid_pos != hex_new.grid_pos:
                            hexes.append(hex_new)
        return hexes

    def visualize_parameters(self, parameter: str ):
        for building in self.buildings:
            building.building_on_hex.change_visualization_parameter(parameter)
            building.draw()
    def draw_buildings(self):
        for building in self.buildings:
            building.draw()
    def calculate_global_parameters(self, ):
        for parameter in ["population", "food", "goods"]:
            param_value = self.calculate_total_parameter(parameter)
            self.global_parameters.change_parameter(parameter, param_value)
            self.statistics[parameter].append(param_value)
    def write_statistics_to_file(self, length: int):
        full_stats  = {"length":length, "global_parameters":self.statistics}
        for idx,building in enumerate(self.buildings):
            full_stats[f"building_{idx}"] = building.building_on_hex.statistics
        with open("statistics.json", "w") as f:
            json.dump(full_stats, f, sort_keys=True, indent=4)
    def calculate_total_parameter(self, parameter: str):
        total = 0
        for building in self.buildings:
            total += building.building_on_hex.get_parameter(parameter)
        return total



    def __str__(self) -> str:
        return f"map with {self.rows} rows and {self.columns} columns"

