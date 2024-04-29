import random
import time
from threading import Thread

from game_content.Sprites import HexagonWheat


class CityGraph:
    def __init__(self, game_map):
        self.game_map = game_map
        self.graph = game_map.create_graph()
        self.year = 1200
        self.medium_temperature = 15

    def calculate_climate(self):
        if self.year < 1300:
            self.medium_temperature -= 0.01
        if self.year >= 1300 and self.year < 1350:
            temperature_delta = random.choice([0.01, 0, -0.01])
            self.medium_temperature += temperature_delta
        if self.year >= 1350:
            self.medium_temperature += 0.01
    def calculate_pandemic(self):
        first_pandemic = True
        if self.year == 1305:
            if first_pandemic:
                pandemic_severity = random.triangular(0.8, 0.9,0.1)
            else:
                pandemic_severity = random.triangular(0.1, 0.2,0.5)
            return pandemic_severity
        return 0


    def calculate(self):
        i = 1
        while i < 10:
            print(i)
            time.sleep(1)
            i+=1
            pandemic_severity = self.calculate_pandemic()
            self.calculate_climate()
            for hex in self.game_map.hexes:
                if isinstance(hex, HexagonWheat):
                    hex.produce()
            for city, neighbours in self.graph.items():
                city.yearly_calculation(pandemic_severity)
            self.game_map.draw_buildings()
            self.game_map.calculate_global_parameters()
        self.game_map.write_statistics_to_file()




    def run_simulation(self):
        t = Thread(target=self.calculate)
        t.start()



        # for sity in self.graph
