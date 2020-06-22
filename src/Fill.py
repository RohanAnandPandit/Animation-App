# -*- coding: utf-8 -*-
"""
Created on Sun Jun 21 19:41:13 2020

@author: rohan
"""
import pygame

class Fill:
    def __init__(self, radius, colour, app):
        self.app = app
        self.radius = radius
        self.colour = colour
        self.listOfCentres = []
    
    def draw(self):
        for centre in self.listOfCentres:
            pygame.draw.circle(self.app.screen, self.colour, centre, self.radius)

    def addPoint(self, point):
        self.listOfCentres.append(point)
