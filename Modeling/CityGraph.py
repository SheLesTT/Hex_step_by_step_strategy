import random
import time
from threading import Thread

import numpy as np
from scipy import stats
from game_content.Sprites import HexagonWheat, Village


class CityGraph:
    def __init__(self, game_map, UI):
        self.game_map = game_map
        self.graph = game_map.create_graph()
        self.year = 1200
        self.medium_temperature = 15
        self.first_pandemic = True
        self.set_nearest_town()
    def set_nearest_town(self,):
        for village in self.graph.keys():
            if isinstance(village, Village):
                if nearest_town := self.game_map.find_nearest_town(self.graph, village):
                    village.set_nearest_town(nearest_town[1])


    def calculate_climate(self):
        if  self.year > 1300 and self.year < 1300:
            self.medium_temperature -= 0.05
        if self.year >= 1300 and self.year < 1350:
            temperature_delta = random.choice([0.01, 0, -0.01])
            self.medium_temperature += temperature_delta
        if self.year >= 1350 and self.year < 1400:
            self.medium_temperature -=0.01
        this_year_temperature = self.medium_temperature + random.uniform(-0.7, 0.7)
        this_year_temperature = this_year_temperature / 15
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
        years = 0
        current_speed = 1
        speed_modifier = 1
        with open('speed.txt', 'w') as f:
            f.write(str(1))
        while self.year < 1500 :
            years += 1
            self.game_map.global_parameters.change_parameter("year", self.year)
            with open('speed.txt', 'r') as f:
                new_modifier = float(f.read())
                if new_modifier != speed_modifier:
                    speed_modifier = new_modifier
                    self.game_map.global_parameters.change_parameter("modeling_speed", speed_modifier)
                    current_speed = 1 / speed_modifier
            time.sleep(current_speed)
            self.year+=1
            pandemic_severity = self.calculate_pandemic()
            this_year_temperature = self.calculate_climate()
            fertility_coef = np.random.normal(this_year_temperature, 0.15)
            # for hex in self.game_map.hexes:
            #     if isinstance(hex, HexagonWheat):
            #         hex.produce()
            for city, neighbours in self.graph.items():
                city.yearly_calculation(pandemic_severity, fertility_coef)
            for city, neighbours in self.graph.items():
                city.migrate()
            self.game_map.draw_buildings()
            self.game_map.calculate_global_parameters()
        self.game_map.write_statistics_to_file(years)




    def run_simulation(self):
        t = Thread(target=self.calculate)
        t.start()



        # for sity in self.graph
