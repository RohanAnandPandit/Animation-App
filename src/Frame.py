# -*- coding: utf-8 -*-
"""
Created on Sun Jun 21 19:39:34 2020

@author: rohan
"""
from Layer import Layer
from pygame import draw


class Frame:
    def __init__(self, app):
        self.app = app
        self.layers = [Layer(self.app)]
        self.current_layer = 0
        self.selected = False
        self.is_background = False

    def show(self, colour=None, show_border=False):
        if self.selected and show_border:
            draw.rect(self.app.get_screen(), (255, 0, 0),
                      (5, 5, self.app.window_width - 15,
                       self.app.window_height - 12), 7)

        for i in range(len(self.layers)):
            self.layers[i].show(colour, i == self.current_layer)

    def get_current_layer(self):
        return self.layers[self.current_layer]

    def add_stroke(self, stroke):
        self.get_current_layer().add_stroke(stroke)

    def add_fill(self, radius, colour):
        self.get_current_layer().addFill(radius, colour)

    def add_image(self, fileLocation):
        self.get_current_layer().add_image(fileLocation)

    def add_layer(self):
        self.layers.append(Layer(self.app))

    def prev_layer(self):
        self.current_layer = max(0, self.current_layer - 1)

    def next_layer(self):
        self.current_layer = min(len(self.layers) - 1,
                                 self.current_layer + 1)

    def undo(self):
        self.get_current_layer().undo()

    def select(self):
        self.selected = True

    def unselect(self):
        try:
            self.selected = False
            self.app.selected_frames.remove(self)
        except:
            pass

    def copy(self):
        del self.app

    def set_background(self, is_background):
        self.is_background = is_background

    def is_background(self):
        return self.is_background
