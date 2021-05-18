# -*- coding: utf-8 -*-
"""
Created on Sun Jun 21 19:44:21 2020

@author: rohan5
"""
from App import App
from Project import Project
import os
import ctypes
from pickle import load
from utils import set_screen
import pygame
import pickle
from utils import APP_PATH

ctypes.windll.shcore.SetProcessDpiAwareness(1)
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (2, 60)
window_width, window_height = 2700, 1700
set_screen(window_width, window_height)
pygame.display.set_caption('Animatis')

try:
    file = open(APP_PATH, 'rb')
    app = pickle.load(file)
    app = App(app.project)
except:
    name = 'untitled'
    project = Project(window_width, window_height, name=name)
    app = App(project)

app.main()
