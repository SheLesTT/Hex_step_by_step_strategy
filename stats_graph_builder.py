import json
import sys
import pygame
import matplotlib
from pygame.locals import *
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

class StatsGraphBuilder():
    def __init__(self, start_date = 1200, years = 9, stats_filename = "statistics.json"):
        self.start_date = start_date
        self.years = years
        self.stats_filename = stats_filename

    def build_matplotlib_graph(self,building, parameter):

        with open(self.stats_filename, "r") as f:
            statistics = json.load(f)
            vis_parameters = statistics[building][parameter]
            figure, axis = plt.subplots()  # Create a figure (the container) and an axis (for plotting)
            axis.plot([self.start_date + i for i in range(self.years)], vis_parameters)  # Plot sample data
            plot_canvas = FigureCanvas(figure)  # Create a canvas to render the Matplotlib plot
            plot_canvas.draw()  # Update the Matplotlib plot if needed
            renderer = plot_canvas.get_renderer()
            matplotlib_plot_rgba_image_data = renderer.tostring_rgb()  # Get raw image data of the plot
            plot_canvas_width, plot_canvas_height = plot_canvas.get_width_height()

            # Convert the Matplotlib image data into a Pygame surface
            plot_surface = pygame.image.fromstring(matplotlib_plot_rgba_image_data,
                                                   (plot_canvas_width, plot_canvas_height),
                                                   "RGB")

            return plot_surface
