# -*- coding: utf-8 -*-
"""
Created on Sun Jun 21 19:43:07 2020

@author: rohan
"""
from pygame import draw, mouse


class ColourPanel:
    def __init__(self, x, y, width, height, columns, colours, app):
        self.app = app
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.columns = columns
        self.swatches = []
        self.create_swatches(colours)
        self.move = False
        self.set_positions()

    def create_swatches(self, colours):
        for colour in colours:
            swatch = ColourSwatch(colour, self)
            self.swatches.append(swatch)

    def set_positions(self):
        swatch_width = int(self.width / self.columns)
        swatch_height = self.height / (len(self.swatches) / self.columns)
        x = self.x
        y = self.y
        for swatch in self.swatches:
            if (x - self.x) >= self.width:
                x = self.x
                y += swatch_height
            swatch.set_values(x, y, swatch_width, swatch_height)
            x += swatch_width

    def show(self):
        for swatch in self.swatches:
            swatch.show()

    def is_mouse_over(self):
        x, y = mouse.get_pos()
        return (self.x <= x <= self.x + self.width and
                self.y <= y <= self.y + self.height)

    def get_selected_colour(self):
        for swatch in self.swatches:
            if swatch.is_mouse_over():
                return swatch.colour

        return None

    def set_cor(self, cor):
        self.x, self.y = cor


class ColourSwatch:
    def __init__(self, colour, colour_panel, x=None, y=None,
                 width=None, height=None):
        self.colour_panel = colour_panel
        self.colour = colour
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def show(self):
        draw.rect(self.colour_panel.app.get_screen(), self.colour,
                  (self.x, self.y, self.width, self.height))
        draw.rect(self.colour_panel.app.get_screen(), (0, 0, 0),
                  (self.x, self.y, self.width, self.height), 1)

    def set_values(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def is_mouse_over(self):
        x, y = mouse.get_pos()
        return (self.x <= x <= self.x + self.width and
                self.y <= y <= self.y + self.height)
