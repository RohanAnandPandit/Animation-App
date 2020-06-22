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
import sys
import os
import shutil
from utils import screenSize, showText, fileLocation

class App:
    def __init__(self, screen):
        self.screen = screen
        (self.windowWidth, self.height) = screenSize()
        self.listOfFrames = []
        self.currentFrame = 0
        self.down = False
        self.width = 2
        self.running = True
        self.update = False
        self.onionSkin = True
        self.colour = (0, 255, 0)
        self.radius = 15
        self.fps = 10
        self.play = False
        self.selectedFrames = []
        self.copiedFrames = []
        self.cut = False
        self.types = ['pen', 'fill']
        self.currentType = 0
        self.colourPanel = ColourPanel(900, 10, 50, 50, 2, self.generateColours(), self)
        self.load()
    
    def generateColours(self):
        colours = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (0, 0, 0), (255, 255, 255)]
        return colours
        
    def getCurrentFrame(self):
        if (len(self.listOfFrames) > 0):
            return self.listOfFrames[self.currentFrame]
    
    def checkEvents(self):
        for event in pygame.event.get():
            if (event.type == pygame.QUIT):
                self.save()
                pygame.quit()
                sys.exit()
                self.running = False
            elif (event.type == pygame.MOUSEBUTTONDOWN):
                if (event.button == 1):
                    self.down = True
                    if (self.colourPanel.isMouseOver()):
                        self.colour = self.colourPanel.getSelectedColour()
                    elif (self.types[self.currentType] == 'pen'):
                        self.getCurrentFrame().addStroke(self.width, self.colour)
                    elif (self.types[self.currentType] == 'fill'):
                        self.getCurrentFrame().addFill(self.radius, self.colour)
                elif (event.button == 3):
                    if (self.colourPanel.isMouseOver()):
                        self.colourPanel.move = True
                    
                    
            elif (event.type == pygame.MOUSEMOTION):
                if (self.down):
                    pos = pygame.mouse.get_pos()
                    self.getCurrentFrame().addPointToFrame(pos)
                    
            elif (event.type == pygame.MOUSEBUTTONUP):
                if (event.button == 1):
                    self.down = False
                elif (event.button == 3):
                    if (self.colourPanel.isMouseOver()):
                        self.colourPanel.move = False
                
            elif (pygame.key.get_pressed()[pygame.K_f] != 0):
                self.currentFrame += 1
                self.insertFrame(self.currentFrame, Frame(self))
                print(self.listOfFrames)
            elif (pygame.key.get_pressed()[pygame.K_l] != 0):
                self.getCurrentFrame().addLayer()
            elif (pygame.key.get_pressed()[pygame.K_o] != 0):
                self.onionSkin = not self.onionSkin
            elif (pygame.key.get_pressed()[pygame.K_s] != 0 
                  and pygame.key.get_pressed()[pygame.K_LCTRL] == 0):
                frame = self.getCurrentFrame() 
                if (frame in self.selectedFrames):
                    frame.unselect()
                else:
                    frame.select()
            elif (pygame.key.get_pressed()[pygame.K_u] != 0):
                print(self.selectedFrames)
                for frame in self.listOfFrames:
                    frame.unselect()
            elif (pygame.key.get_pressed()[pygame.K_BACKSPACE] != 0):
                if (len(self.listOfFrames) > 1):
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
                    self.currentFrame = min(self.currentFrame,
                                            len(self.listOfFrames) - 1)
            elif (pygame.key.get_pressed()[pygame.K_d] != 0):
                frame = self.getCurrentFrame()
                if (len(frame.listOfLayers) > 1):
                    frame.listOfLayers.remove(frame.getCurrentLayer())
                frame.currentLayer = min(frame.currentLayer,
                                         len(frame.listOfLayers) - 1)

            elif (pygame.key.get_pressed()[pygame.K_LEFT] != 0):
                self.prevFrame()
            elif (pygame.key.get_pressed()[pygame.K_RIGHT] != 0):
                self.nextFrame()
            elif (pygame.key.get_pressed()[pygame.K_UP] != 0):
                self.getCurrentFrame().nextLayer()
            elif (pygame.key.get_pressed()[pygame.K_DOWN] != 0):
                self.getCurrentFrame().prevLayer()
            elif (pygame.key.get_pressed()[pygame.K_LCTRL] != 0 
                and pygame.key.get_pressed()[pygame.K_z] != 0):
                self.getCurrentFrame().undo()
            elif (pygame.key.get_pressed()[pygame.K_LCTRL] != 0 
                and pygame.key.get_pressed()[pygame.K_c] != 0):
                self.copyFrames()
            elif (pygame.key.get_pressed()[pygame.K_LCTRL] != 0 
                and pygame.key.get_pressed()[pygame.K_v] != 0):
                self.pasteFrames(self.currentFrame + 1)
            elif (pygame.key.get_pressed()[pygame.K_LCTRL] != 0 
                and pygame.key.get_pressed()[pygame.K_x] != 0):
                self.cutFrames()
            elif (pygame.key.get_pressed()[pygame.K_LCTRL] != 0 
                and pygame.key.get_pressed()[pygame.K_s] != 0):
                self.save()
            elif (pygame.key.get_pressed()[pygame.K_PERIOD] != 0):
                self.currentType = (self.currentType + 1) % len(self.types)
            elif (pygame.key.get_pressed()[pygame.K_EQUALS] != 0):
                penType = self.types[self.currentType]
                if (penType == 'pen'):
                    self.width += 1
                elif (penType == 'fill'):
                    self.radius += 1
            elif (pygame.key.get_pressed()[pygame.K_MINUS] != 0):
                penType = self.types[self.currentType]
                if (penType == 'pen'):
                    self.width = max(0, self.width - 1)
                elif (penType == 'fill'):
                    self.radius = max(0, self.radius - 1)
            
            
                
        if (pygame.key.get_pressed()[pygame.K_SPACE] != 0):
            self.playAnimation(self.currentFrame)

    def insertFrame(self, index, frame):
        self.listOfFrames.insert(index, frame)
    
    def cutFrames(self):
        if (len(self.copiedFrames) < len(self.listOfFrames)):
            self.copyFrames()
            for frame in self.selectedFrames:
                self.listOfFrames.remove(frame)
                
            self.currentFrame = min(self.currentFrame, len(self.listOfFrames) - 1)
            self.selectedFrames = []
            self.cut = True
            
    def pasteFrames(self, index):
        for frame in self.copiedFrames:
            self.listOfFrames.insert(index, copy.deepcopy(frame))
            index += 1
            
        if (self.cut):
            self.copiedFrames = []
            self.cut = False
    
    def copyFrames(self):
        self.copiedFrames = self.selectedFrames.copy()
        
    def prevFrame(self):
        self.currentFrame = self.currentFrame - 1
        if (self.currentFrame == -1):
            self.currentFrame = len(self.listOfFrames) - 1

    def nextFrame(self):
        self.currentFrame = (self.currentFrame + 1) % len(self.listOfFrames)
        
    def showOnionSkin(self):
        if (self.currentFrame > 1):
            frame = self.listOfFrames[self.currentFrame - 2]
            # .listOfLayers[frame.currentLayer]
            frame.show((230, 230, 255), False)
        if (self.currentFrame > 0):
            frame = self.listOfFrames[self.currentFrame - 1]
            # .listOfLayers[frame.currentLayer]
            frame.show((255, 180, 180), False)
        if (self.currentFrame < len(self.listOfFrames) - 1):
            frame = self.listOfFrames[self.currentFrame + 1]
            # .listOfLayers[frame.currentLayer]
            frame.show((180, 255, 180), False)
    
    def playAnimation(self, start):
        screen.fill((255, 255, 255))
        for i in range(start, len(self.listOfFrames)):
            frame =  self.listOfFrames[i]
            frame.show()
            pygame.display.update()
            
            if (pygame.key.get_pressed()[pygame.K_SPACE] == 0):
                return
            
            time.sleep(1/self.fps)
            screen.fill((255, 255, 255))
    
    def showInfo(self):
        text = 'Frame ' + str(self.currentFrame+1) + ' of '
        text += str(len(self.listOfFrames))
        showText(self.screen, text, 100, 30, fontSize = 30)
        
        text = 'Layer ' + str(self.getCurrentFrame().currentLayer+1) + ' of '
        text += str(len(self.getCurrentFrame().listOfLayers))
        showText(self.screen, text, 300, 30, fontSize = 30)        
    
    def undo(self):
        self.getCurrentFrame().undo()
    
    def save(self):
        if (os.path.exists(fileLocation)):
            if (os.path.exists(fileLocation+'/')):
                shutil.rmtree(fileLocation+'/', True)
        #if (not os.path.exists(fileLocation)):
        try:
            os.mkdir(fileLocation)
        except:
            pass
        if (not os.path.exists(fileLocation+'/Frames')): 
            os.mkdir(fileLocation+'/Frames')
        frameIndex = 1
        for frame in self.listOfFrames:
            frameLocation = fileLocation+'/Frames/Frame'+str(frameIndex)
            os.mkdir(frameLocation)
            layerIndex = 1 
            for layer in frame.listOfLayers:
                layerLocation = frameLocation+'/Layer'+str(layerIndex)
                os.mkdir(layerLocation)
                objectsFile = open(layerLocation+'/Objects.txt', 'w')
                for obj in layer.listOfObjects:
                    if (type(obj) == Stroke):
                        objectsFile.write('Stroke|'+str(obj.colour)+'|'+str(obj.listOfPoints)+'\n')
                    elif (type(obj) == Fill):
                        objectsFile.write('Fill|'+str(obj.colour)+'|'+str(obj.listOfCentres)+'\n')
                objectsFile.close()
                layerIndex += 1
            frameIndex += 1

    def load(self):
        frameIndex = 1
        while (True):
            frameLocation = fileLocation+'/Frames/Frame'+str(frameIndex)
            if (os.path.exists(frameLocation)):
                frame = Frame(self)
                layerIndex = 1 
                layers = []
                while (True):
                    layerLocation = frameLocation+'/Layer'+str(layerIndex)
                    if (os.path.exists(layerLocation)):
                        layer = Layer(self)
                        objects = []
                        objectsFile = open(layerLocation+'/Objects.txt','r')
                        for points in objectsFile:
                            point = points.split('|')
                            if (point[0] == 'Stroke'):
                                obj = Stroke(self.width, eval(point[1]), self)
                                obj.listOfPoints = eval(point[2])
                            elif (point[0] == 'Fill'):
                                obj = Fill(self.radius, eval(point[1]), self)
                                obj.listOfCentres = eval(point[2])
                            objects.append(obj)
                        objectsFile.close()
                        layer.listOfObjects = objects.copy()
                        layers.append(layer)
                    else:
                        break
                    layerIndex += 1
                frame.listOfLayers = layers.copy()
                self.listOfFrames.append(frame)
            else:
                break
            frameIndex += 1
        if (self.listOfFrames == []):
            self.listOfFrames.append(Frame())
        
    def main(self):
        while (self.running):
            self.screen.fill((255, 255, 255))
            self.checkEvents()
            if (self.onionSkin):
                self.showOnionSkin()
            self.getCurrentFrame().show(None, True)
            self.showInfo()
            if (self.colourPanel.move):
                (self.colourPanel.x, self.colourPanel.y) = pygame.mouse.get_pos()
                self.colourPanel.setPositions()
            self.colourPanel.show()
            pygame.display.update()
  