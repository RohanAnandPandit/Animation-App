# -*- coding: utf-8 -*-
"""
Created on Sun Jun 21 19:40:02 2020

@author: rohan
"""
from Stroke import Stroke


class Layer:
    def __init__(self, app):
        self.app = app
        self.visible = True
        self.objects = []

    def show(self, colour=None, is_current=False):
        if self.visible:
            for obj in self.objects:
                if type(obj) == Stroke:
                    obj.draw(None, colour, is_current)
                else:
                    obj.draw()

    def add_stroke(self, stroke):
        self.add_object(stroke)

    '''
    def addFill(self, radius, colour):
        self.addObject(Fill(radius, colour, self.app))
    '''

    def add_image(self, fileLocation):
        self.listOfImages.append(fileLocation)

    def undo(self):
        if len(self.objects) > 0:
            del self.objects[len(self.objects) - 1]

    def add_object(self, obj):
        self.objects.append(obj)

    def get_strokes(self):
        return self.objects
