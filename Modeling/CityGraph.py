import time


class CityGraph:
    def __init__(self, game_map):
        self.game_map = game_map
        self.graph = game_map.create_graph()

    def run_simulation(self):
        i= 0
        while i < 100:
            i+=1
            for city, neighbours in self.graph.items():
                neighbours = [neighbour[0] for neighbour in neighbours]
                for neighbour in neighbours:
                    if city.population < neighbour.population:
                        city.population += 1
                        neighbour.population -= 1

        # for sity in self.graph
