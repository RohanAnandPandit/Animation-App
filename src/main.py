# -*- coding: utf-8 -*-
"""
Created on Sun Jun 21 19:44:21 2020

@author: rohan
"""
import pygame
from App import App
import sys
import os
import ctypes
from utils import screenSize, setScreen
import pickle 

ctypes.windll.shcore.SetProcessDpiAwareness(1)
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (2, 60) 

windowWidth, windowHeight = screenSize()
windowWidth -= 5
windowHeight -= 80
screen = setScreen(windowWidth, windowHeight)
pygame.display.set_caption('Anim8')
screen.fill((255, 255, 255))

file = open('my_animation', 'rb')
app = pickle.load(file)
file.close()

app = App(windowWidth, windowHeight)
app.main()