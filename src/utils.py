# -*- coding: utf-8 -*-
"""
Created on Sun Jun 21 19:50:54 2020

@author: rohan
"""
from tkinter import *
import pygame

fileLocation = "C:/Rohan Pandit/COMPUTER SCIENCE/Animation App/my_animation"
def screenSize():
    test = Tk()
    width = test.winfo_screenwidth()
    height = test.winfo_screenheight()-75 # Takes the toolbar into account
    test.destroy()
    return (width, height)

def showText(screen, text = 'text box', centreX = 0, centreY = 0,
             fontColour = (0, 0, 0), fontBg = (255, 255, 255), fontSize = 10):
    # initialises font for displaying text
    basicfont = pygame.font.SysFont('unifont.ttf', fontSize) 
    text = basicfont.render(text, True, fontColour, fontBg)
    textrect = text.get_rect()
    textrect.center = (centreX,centreY) # 
    screen.blit(text, textrect) # Shows text on screen

def showImage(image, x, y):
    image = pygame.image.load(fileLocation + image + '.jpg').convert()
    screen.blit(image, (x,y))
    
def averageOfColour(colour):
    (r, g, b) = (colour[0], colour[1], colour[2])
    avg = int((r + g + b) / 3)
    return (255 - avg, 255 - avg, 255 - avg)

