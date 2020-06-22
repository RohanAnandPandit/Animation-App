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
from utils import screenSize
import shutil

ctypes.windll.shcore.SetProcessDpiAwareness(1)
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (2,28) 
screen = pygame.display.set_mode(screenSize())
pygame.display.set_caption('Anim8')
screen.fill((255, 255, 255))
app = App(screen)
app.main()