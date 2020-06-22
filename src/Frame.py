# -*- coding: utf-8 -*-
"""
Created on Sun Jun 21 19:39:34 2020

@author: rohan
"""
import pygame
from Layer import Layer

class Frame:
    def __init__(self, app):
        self.app = app
        self.listOfLayers = [Layer(self.app)]
        self.currentLayer = 0
        self.selected = False
    
    def show(self, colour = None, showBorder = False):
        if (self.selected and showBorder):
            pygame.draw.rect(self.app.screen, (255, 0, 0),
                             (5, 5, self.app.windowWidth - 15, self.app.height - 12), 7)
        for i in range(len(self.listOfLayers)):
            self.listOfLayers[i].show(colour, i == self.currentLayer)
            
    def getCurrentLayer(self):
        return self.listOfLayers[self.currentLayer]
        
    def addPointToFrame(self, point):
        self.getCurrentLayer().addPointToLayer(point)
    
    def addStroke(self, width, colour):
        self.getCurrentLayer().addStroke(width, colour)

    def addFill(self, radius, colour):
        self.getCurrentLayer().addFill(radius, colour)

    def addImage(self, fileLocation):
        self.getCurrentLayer().addImage(fileLocation)
    
    def addLayer(self):
        self.listOfLayers.append(Layer(self.app))
    
    def prevLayer(self):
        self.currentLayer = max(0, self.currentLayer - 1)

    def nextLayer(self):
        self.currentLayer = min(len(self.listOfLayers) - 1,
                                self.currentLayer + 1)                   
    def undo(self):
        self.getCurrentLayer().undo()
    
    def select(self):
        app.selectedFrames.append(self)
        self.selected = True
        
    def unselect(self):
        try:
            app.selectedFrames.remove(self)
        except ValueError:
            pass
        self.selected = False
        