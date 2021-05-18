# -*- coding: utf-8 -*-
"""
Created on Sun Jun 21 19:40:27 2020

@author: rohan
"""
from pygame import draw


class Stroke:
    def __init__(self, width, colour, app, points=None):
        self.app = app
        self.points = points
        if points is None:
            self.points = []
        self.width = width
        self.colour = colour

    def draw(self, width=None, colour=None, is_current=False):
        if colour is None:
            colour = self.colour
            if not is_current:
                colour = (100, 100, 100)

        if width is None:
            width = self.width

        if len(self.points) == 1:
            if width == 0:
                draw.aaline(self.app.get_screen(), colour,
                            self.points[0],
                            self.points[0])
            else:
                draw.line(self.app.get_screen(), colour,
                          self.points[0],
                          self.points[0])

        for i in range(1, len(self.points)):
            if width == 0:
                draw.aaline(self.app.get_screen(), colour,
                            self.points[i - 1],
                            self.points[i])
            else:
                draw.line(self.app.get_screen(), colour,
                          self.points[i - 1],
                          self.points[i], width)

    def add_point(self, point):
        self.points.append(point)

    def get_points(self):
        return self.points
