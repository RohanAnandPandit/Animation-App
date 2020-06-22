# -*- coding: utf-8 -*-
"""
Created on Sun Jun 21 19:43:07 2020

@author: rohan
"""
import pygame

class ColourPanel:
    def __init__(self, x, y, width, height, columns, colours, app):
        self.app = app
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.columns = columns
        self.listOfSwatches = []
        self.createSwatches(colours)
        self.move = False
        self.setPositions()
    
    def createSwatches(self, colours):
        for colour in colours:
            swatch = ColourSwatch(colour, self)
            self.listOfSwatches.append(swatch)

    def setPositions(self):
        swatchWidth = int(self.width / self.columns)
        swatchHeight = self.height / (len(self.listOfSwatches) / self.columns)
        x = self.x
        y = self.y
        for swatch in self.listOfSwatches:
            if ((x - self.x) >= self.width):
                x = self.x
                y += swatchHeight
            swatch.setValues(x, y, swatchWidth, swatchHeight)
            x += swatchWidth
    
    def show(self):
        for swatch in self.listOfSwatches:
            swatch.show()
            
    def isMouseOver(self):
        (x, y) = pygame.mouse.get_pos()
        return self.x <= x <= self.x + self.width and self.y <= y <= self.y + self.height
    
    def getSelectedColour(self):
        for swatch in self.listOfSwatches:
            if (swatch.isMouseOver()):
                return swatch.colour
        return None
            
class ColourSwatch:
    def __init__(self, colour, colourPanel):
        self.colourPanel = colourPanel
        self.colour = colour
    
    def show(self):
        pygame.draw.rect(self.colourPanel.app.screen, self.colour,
                         (self.x, self.y, self.width, self.height))
        pygame.draw.rect(self.colourPanel.app.screen, (0, 0, 0),
                         (self.x, self.y, self.width, self.height), 1)
    
    def setValues(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        
    def isMouseOver(self):
        (x, y) = pygame.mouse.get_pos()
        return self.x <= x <= self.x + self.width and self.y <= y <= self.y + self.height

