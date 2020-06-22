# -*- coding: utf-8 -*-
"""
Created on Sun Jun 21 19:40:27 2020

@author: rohan
"""
import pygame

class Stroke:
    def __init__(self, width, colour, app):
        self.app = app
        self.listOfPoints = []
        self.width = width
        self.colour = colour

    def draw(self, width = None, colour = None, isCurrent = False):
        if (colour == None):
            colour = self.colour
            if (not isCurrent):
                colour = (100, 100, 100)
        if (width == None):
            width = self.width
            
        if (len(self.listOfPoints) == 1):
            if (width == 0):
                pygame.draw.aaline(self.app.screen, colour, self.listOfPoints[0], 
                                   self.listOfPoints[0])   
            else:
                pygame.draw.line(self.app.screen, colour, self.listOfPoints[0], 
                                   self.listOfPoints[0])                  
        for i in range(1, len(self.listOfPoints)):
            if (width == 0):
                pygame.draw.aaline(self.app.screen, colour, self.listOfPoints[i - 1],
                                 self.listOfPoints[i])   
            else:
                pygame.draw.line(self.app.screen, colour, self.listOfPoints[i - 1],
                                 self.listOfPoints[i], width)    

    
    def addPoint(self, point):
        self.listOfPoints.append(point)
