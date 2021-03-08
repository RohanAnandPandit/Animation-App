# -*- coding: utf-8 -*-
"""
Created on Sun Jun 21 19:38:03 2020

@author: rohan
"""
from Frame import Frame
from Layer import Layer
from Stroke import Stroke
from Fill import Fill
from Colour_Panel import ColourPanel, ColourSwatch
import pygame 
pygame.init()
pygame.font.init()
import sys
import os
import shutil
from utils import screenSize, showText, fileLocation
import copy
import time 
import utils

class App:
    def __init__(self, windowWidth, windowHeight):
        self.windowWidth, self.windowHeight = windowWidth, windowHeight
        self.listOfFrames = [Frame(self)]
        self.currentFrame = 0
        self.down = False
        self.width = 2
        self.running = True
        self.update = False
        self.onionSkin = True
        self.colour = (0, 0, 0)
        self.radius = 15
        self.fps = 15
        self.play = False
        self.selectedFrames = []
        self.copiedFrames = []
        self.cut = False
        self.types = ['pen', 'fill']
        self.currentType = 0
        self.currentStroke = Stroke(self.width, self.colour, self)
        self.colourPanel = ColourPanel(900, 10, 50, 50, 2,
                                       self.generateColours(), self)
        self.active = False
        self.clearScreen = False
    
    def getScreen(self):
        return utils.screen
    
    def generateColours(self):
        colours = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (0, 0, 0),
                   (255, 255, 255)]
        return colours
        
    def getCurrentFrame(self):
        if len(self.listOfFrames) > 0:
            return self.listOfFrames[self.currentFrame]
    
    def checkEvents(self):
        for event in pygame.event.get():
            
            if event.type == pygame.QUIT:
                self.save()
                pygame.quit()
                sys.exit()
                self.running = False
                
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.active = True
                
                if event.button == 1:
                    self.down = True
                    if self.colourPanel.isMouseOver():
                        
                        self.colour = self.colourPanel.getSelectedColour()
                        
                    elif self.types[self.currentType] == 'pen':
                        self.currentStroke.addPoint(pygame.mouse.get_pos())
                        
                    elif self.types[self.currentType] == 'fill':
                        self.getCurrentFrame().addFill(self.radius, self.colour)
                        
                elif event.button == 3:
                    if self.colourPanel.isMouseOver():
                        self.colourPanel.move = True
                    
                    
            elif event.type == pygame.MOUSEMOTION:
                if self.down:
                    self.currentStroke.addPoint(pygame.mouse.get_pos())
            
            elif event.type == pygame.MOUSEBUTTONUP:
                self.active = False
                if event.button == 1:
                    self.down = False
                    self.getCurrentFrame().addStroke(self.currentStroke)
                    self.currentStroke = Stroke(self.width, self.colour, self)
                    
                elif event.button == 3:
                    if self.colourPanel.isMouseOver():
                        self.colourPanel.move = False
                        
            elif event.type == pygame.KEYDOWN:
                self.clearScreen = self.active = True
                #print(self.clearScreen)
                if pygame.key.get_pressed()[pygame.K_f] != 0:
                    self.currentFrame += 1
                    self.insertFrame(self.currentFrame, Frame(self))
                    print(self.listOfFrames)
                    
                elif (pygame.key.get_pressed()[pygame.K_l] != 0):
                    self.getCurrentFrame().addLayer()
                    
                elif pygame.key.get_pressed()[pygame.K_o] != 0:
                    self.onionSkin = not self.onionSkin
                    
                elif (pygame.key.get_pressed()[pygame.K_s] 
                      and not pygame.key.get_pressed()[pygame.K_LCTRL]):
                    frame = self.getCurrentFrame() 
                    
                    if frame.selected:
                        frame.unselect()
                        
                    else:
                        frame.select()
                        self.selectedFrames.append(frame)
                        
                elif pygame.key.get_pressed()[pygame.K_u]:
                    print(self.selectedFrames)
                    for frame in self.listOfFrames:
                        frame.unselect()
                        
                elif pygame.key.get_pressed()[pygame.K_BACKSPACE]:
                    if len(self.listOfFrames) > 0:
                        frame = self.getCurrentFrame()
                        self.listOfFrames.remove(frame)
                        
                        try:
                            self.selectedFrames.remove(frame)
                        except:
                            pass
                        
                        try:
                            self.copiedFrames.remove(frame)
                        except:
                            pass
                        
                        if len(self.listOfFrames) == 0:
                            self.listOfFrames = [Frame(self)]
                        else:
                            self.currentFrame = min(self.currentFrame,
                                                   len(self.listOfFrames) - 1)
                    
                        
                elif pygame.key.get_pressed()[pygame.K_d]:
                    frame = self.getCurrentFrame()
                    if len(frame.listOfLayers) > 1:
                        frame.listOfLayers.remove(frame.getCurrentLayer())
                    frame.currentLayer = min(frame.currentLayer,
                                             len(frame.listOfLayers) - 1)
    
                elif pygame.key.get_pressed()[pygame.K_LEFT]:
                    self.prevFrame()
                    
                elif pygame.key.get_pressed()[pygame.K_RIGHT]:
                    self.nextFrame()
                    
                elif pygame.key.get_pressed()[pygame.K_UP]:
                    self.getCurrentFrame().nextLayer()
                    
                elif pygame.key.get_pressed()[pygame.K_DOWN]:
                    self.getCurrentFrame().prevLayer()
                    
                elif (pygame.key.get_pressed()[pygame.K_LCTRL] 
                    and pygame.key.get_pressed()[pygame.K_z]):
                    self.getCurrentFrame().undo()
                    
                elif (pygame.key.get_pressed()[pygame.K_LCTRL]
                    and pygame.key.get_pressed()[pygame.K_c]):
                    self.copyFrames()
                    
                elif (pygame.key.get_pressed()[pygame.K_LCTRL] 
                    and pygame.key.get_pressed()[pygame.K_v]):
                    print(self.currentFrame)
                    self.pasteFrames(self.currentFrame + 1)
                    
                elif (pygame.key.get_pressed()[pygame.K_LCTRL] 
                    and pygame.key.get_pressed()[pygame.K_x]):
                    self.cutFrames()
                    
                elif (pygame.key.get_pressed()[pygame.K_LCTRL] 
                    and pygame.key.get_pressed()[pygame.K_s]):
                    self.save()
                    
                elif pygame.key.get_pressed()[pygame.K_PERIOD]:
                    self.currentType = (self.currentType + 1) % len(self.types)
                    
                elif pygame.key.get_pressed()[pygame.K_EQUALS]:
                    penType = self.types[self.currentType]
                    
                    if penType == 'pen':
                        self.width += 1
                        
                    elif penType == 'fill':
                        self.radius += 1
                        
                elif pygame.key.get_pressed()[pygame.K_MINUS]:
                    penType = self.types[self.currentType]
                    
                    if (penType == 'pen'):
                        self.width = max(0, self.width - 1)
                        
                    elif (penType == 'fill'):
                        self.radius = max(0, self.radius - 1)
            
            
                
        if pygame.key.get_pressed()[pygame.K_SPACE]:
            self.playAnimation(self.currentFrame)

    def insertFrame(self, index, frame):
        self.listOfFrames.insert(index, frame)
    
    def cutFrames(self):
        if len(self.copiedFrames) < len(self.listOfFrames):
            self.copyFrames()
            
            for frame in self.selectedFrames:
                self.listOfFrames.remove(frame)
                
            self.currentFrame = min(self.currentFrame, 
                                    len(self.listOfFrames) - 1)
            self.selectedFrames = []
            self.cut = True
            
    def pasteFrames(self, index):
        print(self.copiedFrames)
        for frame in self.copiedFrames:
            print(index, frame)
            self.listOfFrames.insert(index, copy.deepcopy(frame))
            index += 1
            
        if self.cut:
            self.copiedFrames = []
            self.cut = False
    
    def copyFrames(self):
        self.copiedFrames = self.selectedFrames.copy()
        
    def prevFrame(self):
        self.currentFrame = self.currentFrame - 1
        
        if self.currentFrame == -1:
            self.currentFrame = len(self.listOfFrames) - 1

    def nextFrame(self):
        self.currentFrame = (self.currentFrame + 1) % len(self.listOfFrames)
        
    def showOnionSkin(self):
        if self.currentFrame > 1:
            frame = self.listOfFrames[self.currentFrame - 2]
            # .listOfLayers[frame.currentLayer]
            frame.show((230, 230, 255), False)
            
        if self.currentFrame > 0:
            frame = self.listOfFrames[self.currentFrame - 1]
            # .listOfLayers[frame.currentLayer]
            frame.show((255, 180, 180), False)
            
        if self.currentFrame < len(self.listOfFrames) - 1:
            frame = self.listOfFrames[self.currentFrame + 1]
            # .listOfLayers[frame.currentLayer]
            frame.show((180, 255, 180), False)
    
    def playAnimation(self, start):
        for i in range(start, len(self.listOfFrames)):
            self.getScreen().fill((255, 255, 255))
            frame =  self.listOfFrames[i]
            frame.show()
            pygame.display.update()
            
            if not pygame.key.get_pressed()[pygame.K_SPACE]:
                return
            
            time.sleep(1 / self.fps)
            
    
    def showInfo(self):
        from main import screen
        
        text = 'Frame ' + str(self.currentFrame + 1) + ' of '
        text += str(len(self.listOfFrames))
        showText(screen, text, 100, 30, fontSize = 30)
        
        text = 'Layer ' + str(self.getCurrentFrame().currentLayer + 1) + ' of '
        text += str(len(self.getCurrentFrame().listOfLayers))
        showText(screen, text, 300, 30, fontSize = 30)        
    
    def undo(self):
        self.getCurrentFrame().undo()
        
    def save(self):
        import pickle
        
        with open('my_animation', 'wb') as file:
            pickle.dump(self, file)
        
        
    def show(self):
        if self.onionSkin:
            self.showOnionSkin() 
            
        if self.active:
                
            if self.clearScreen:
                self.getScreen().fill((255, 255, 255))
                self.getCurrentFrame().show(colour = None, 
                                            showBorder = True)
                
            self.currentStroke.draw(colour = self.colour)
            
         
        if self.clearScreen:
            self.showInfo()
            
            if self.colourPanel.move:
                self.colourPanel.setCor(pygame.mouse.get_pos())
                self.colourPanel.setPositions()
                
            self.colourPanel.show()
        
        self.clearScreen = False
            
        pygame.display.update()
        
    def main(self):
        self.showInfo()
        self.colourPanel.show()
        self.showOnionSkin()
        self.getCurrentFrame().show(colour = None, showBorder = True)
        
        while self.running:
            self.checkEvents()
            self.show()
                            

                
  