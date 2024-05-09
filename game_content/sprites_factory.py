from math import sin, cos, sqrt, pi, floor

import pygame

from game_content.Sprites import HexagonLand, HexagonSea, HexagonMountain, HexagonEmpty, Hexagon, Town, \
    OffsetCoordinates, HexagonForest, HexagonGrape, HexagonWheat, HexagonSheep, Village


class HexPointsStorage():
    def __init__(self,):


        self.hex_side = 15 * sqrt(3)
        self.width = 30 * sqrt(3)
        self.height = self.width / 2 * sqrt(3)
        self.points = self.calculate_points_for_hexagon()
        self.points_for_road = self.calculate_points_for_road()
        self.points_for_river = self.calculate_points_for_river()

    def calculate_points_for_hexagon(self):
        points = []
        v = 0
        for i in range(6):
            points.append((round(cos(v) * (self.width // 2) + self.width / 2, 2),
                           round(sin(v) * (self.width // 2) + self.width / 2 - (self.width - self.height) / 2, 2)))
            v += (pi * 2) / 6
        return points

    def calculate_points_for_road(self,  line_thickness=4):
        p = [pygame.Vector2(point) for point in self.points]
        side = self.hex_side / 2 - line_thickness / 2
        big_side = side * sqrt(3) / 2
        small_side = side * 0.5
        road_1_p0 = p[2] + (side, 0)
        road_1_p3 = p[1] + (-side, 0)
        road_2_p0 = p[3] + (small_side, big_side)
        road_2_p3 = p[2] + (-small_side, -big_side)
        road_3_p0 = p[4] + (-small_side, big_side)
        road_3_p3 = p[3] + (small_side, -big_side)
        road_4_p0 = p[5] + (-side, 0)
        road_4_p3 = p[4] + (side, 0)
        road_5_p0 = p[0] + (-small_side, -big_side)
        road_5_p3 = p[5] + (small_side, big_side)
        road_0_p0 = p[1] + (small_side, -big_side)
        road_0_p3 = p[0] + (-small_side, big_side)
        center = (p[2] + (floor(self.hex_side / 2), -self.hex_side / 2 * sqrt(3)))
        small_center_side = line_thickness / 2
        large_center_side = small_center_side * sqrt(3)
        center_point_0 = center + (large_center_side, 0)
        center_point_1 = center + (small_center_side, large_center_side)
        center_point_2 = center + (-small_center_side, large_center_side)
        center_point_3 = center + (-large_center_side, 0)
        center_point_4 = center + (-small_center_side, -large_center_side)
        center_point_5 = center + (small_center_side, -large_center_side)

        points_for_river = {0: [road_0_p0, center_point_3, center_point_4, road_0_p3],
                            1: [road_1_p0, center_point_4, center_point_5, road_1_p3],
                            2: [road_2_p0, center_point_5, center_point_0, road_2_p3],
                            3: [road_3_p0, center_point_0, center_point_1, road_3_p3],
                            4: [road_4_p0, center_point_1, center_point_2, road_4_p3],
                            5: [road_5_p0, center_point_2, center_point_3, road_5_p3],
                            6: center}

        return points_for_river


    def calculate_points_for_river(self, river_thickness: int = 3, ):

        river_thickness = river_thickness
        another_side = sqrt(3)
        point_0_left = (self.points[0][0] - another_side, self.points[0][1] + river_thickness)
        point_0_right = (self.points[0][0] - another_side, self.points[0][1] - river_thickness)
        point_1_left = (self.points[1][0] - river_thickness, self.points[1][1])
        point_1_right = (self.points[1][0] + another_side, self.points[1][1] - river_thickness)
        point_2_left = (self.points[2][0] - another_side, self.points[2][1] - river_thickness)
        point_2_right = (self.points[2][0] + river_thickness, self.points[2][1])
        point_3_left = (self.points[3][0] + another_side, self.points[3][1] - river_thickness)
        point_3_right = (self.points[3][0] + another_side, self.points[3][1] + river_thickness)
        point_4_left = (self.points[4][0] + river_thickness, self.points[4][1])
        point_4_right = (self.points[4][0] - another_side, self.points[4][1] + river_thickness)
        point_5_left = (self.points[5][0] + another_side, self.points[5][1] + river_thickness)
        point_5_right = (self.points[5][0] - river_thickness, self.points[5][1])

        points_for_triangle = {0: [self.points[0], point_0_right, point_1_left, self.points[1]],
                               1: [self.points[1], point_1_right, point_2_left, self.points[2]],
                               2: [self.points[2], point_2_right, point_3_left, self.points[3]],
                               3: [self.points[3], point_3_right, point_4_left, self.points[4]],
                               4: [self.points[4], point_4_right, point_5_left, self.points[5]],
                               5: [self.points[5], point_5_right, point_0_left, self.points[0]]}

        return points_for_triangle

    def get_points_for_river(self, triangle_index):
        return self.points_for_river[triangle_index]

    def get_points_for_road(self, triangle_index):
        return self.points_for_road[triangle_index]


class HexesFactory():
    def __init__(self, game_map):
        self.storage = HexPointsStorage()
        self.game_map = game_map

    def create_hex(self, hex_params: str | dict, grid_pos: OffsetCoordinates,loading=False) -> Hexagon:
        hex_type = hex_params["type"]
        match hex_type:
            case "HexagonLand":
                hex_created = (HexagonLand(grid_pos, self.storage, self.game_map))
            case "HexagonSea":
                hex_created = (HexagonSea(grid_pos, self.storage, self.game_map))
            case "HexagonMountain":
                hex_created = (HexagonMountain(grid_pos, self.storage, self.game_map))
            case "HexagonEmpty":
                hex_created = (HexagonEmpty(grid_pos, self.storage, game_map=self.game_map))
            case "HexagonForest":
                hex_created = (HexagonForest(grid_pos, self.storage, self.game_map))
            case "HexagonGrape":
                hex_created = (HexagonGrape(grid_pos, self.storage, self.game_map))
            case "HexagonSheep":
                hex_created = (HexagonSheep(grid_pos, self.storage, self.game_map))
            case "HexagonWheat":
                fertility = hex_params.get('fertility')
                mod = hex_params.get('mod')
                hex_created = (HexagonWheat(grid_pos, self.storage, self.game_map, fertility, mod))


            case _:

                hex_created = (HexagonLand(grid_pos, self.storage, self.game_map))

        self.add_items_on_hex(hex_created, hex_params,loading=loading)
        return hex_created

    def add_items_on_hex(self, hex_created: Hexagon, hex_params: dict,loading=False) -> None:
        if hex_params.get("building_on_hex"):
            self.add_building(hex_created, hex_params["building_on_hex"],loading)
        if hex_params.get("roads"):
            hex_created.roads = hex_params["roads"]
        if hex_params.get("rivers"):
            hex_created.rivers = hex_params["rivers"]


    def add_building(self, hex_created: Hexagon, building: dict,loading=False) -> None:
        match building["name"]:
            case "Town":
                created_building = Town(hex_created.grid_pos, self.game_map)
            case "Village":
                created_building = Village(hex_created.grid_pos, self.game_map, loading=loading)
            case _:
                pass
        data = building["data"]
        created_building.population = data["population"]
        created_building.food = data["food"]
        created_building.goods = data["goods"]
        hex_created.building_on_hex = created_building

    def replace_hex(self, hex_type: str, grid_pos: OffsetCoordinates, old_hex: Hexagon) -> Hexagon:
        hex_save = old_hex.save_to_json()
        hex_save.update({'type':hex_type})
        hex_created = self.create_hex(hex_save, grid_pos)
        hex_created.neighbours = old_hex.neighbours
        for direction, neighbour in enumerate(hex_created.neighbours):
            reversed_direction =  (direction+ 3) % 6
            try:
                neighbour.neighbours[reversed_direction] = hex_created
            except IndexError:
                print("Error","Direction number  was", reversed_direction)
        hex_created.draw()
        return hex_created
