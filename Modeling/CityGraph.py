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
        self.first_pandemic = True

    def calculate_climate(self):
        if self.year < 1300:
            self.medium_temperature -= 0.05
        if self.year >= 1300 and self.year < 1350:
            temperature_delta = random.choice([0.01, 0, -0.01])
            self.medium_temperature += temperature_delta
        if self.year >= 1350 and self.year < 1400:
            self.medium_temperature -= 0.05
        this_year_temperature = self.medium_temperature + random.uniform(-0.7, 0.7)
        return this_year_temperature
    def calculate_pandemic(self):
        if self.year >= 1320 :
            if self.first_pandemic:
                if random.uniform(0, 1) < 0.03:
                    self.first_pandemic = False
                    pandemic_severity = random.triangular(0.8, 0.9,0.1)
                    self.years_without_pandemic = 0
                    return pandemic_severity
            else:
                self.years_without_pandemic += 1.
                if self.years_without_pandemic > 20:
                    if random.uniform(0, 1) < 0.03:
                        pandemic_severity = random.triangular(0.1, 0.2,0.5)
                        return pandemic_severity
        return 0


    def calculate(self):
        while self.year < 1210 :
            time.sleep(1)
            self.year+=1
            pandemic_severity = self.calculate_pandemic()
            this_year_temperature = self.calculate_climate()
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
