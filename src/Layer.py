# -*- coding: utf-8 -*-
"""
Created on Sun Jun 21 19:40:02 2020

@author: rohan
"""
from Stroke import Stroke
from Fill import Fill

class Layer:
    def __init__(self, app):
        self.app = app
        self.visible = True
        self.listOfObjects = []
        
    def show(self, colour = None, isCurrent = False):
        if self.visible:
            for obj in self.listOfObjects:
                if (type(obj) == Stroke):
                    obj.draw(None, colour, isCurrent)
                else:
                    obj.draw()
                
    def addPointToLayer(self, point):
        if len(self.listOfObjects) > 0:
            self.listOfObjects[len(self.listOfObjects) - 1].addPoint(point)
    
    def addStroke(self, stroke):
        self.addObject(stroke)
    
    def addFill(self, radius, colour):
        self.addObject(Fill(radius, colour, self.app))

    def addImage(self, fileLocation):
        self.listOfImages.append(fileLocation)

    def undo(self):
        if (len(self.listOfObjects) > 0):
            del self.listOfObjects[len(self.listOfObjects) - 1]

    def addObject(self, obj):
        self.listOfObjects.append(obj)