# -*- coding: utf-8 -*-
"""
Created on Sun Jun 21 19:50:54 2020

@author: rohan
"""
from tkinter import Tk
from pygame import font, display, RESIZABLE
from pygame import image as py_image

fileLocation = "C:/Rohan Pandit/COMPUTER SCIENCE/Animation App/my_animation"
screen = None
APP_PATH = 'animation_app'


def screen_size():
    test = Tk()
    width = test.winfo_screenwidth()
    height = test.winfo_screenheight() - 75  # Takes the toolbar into account
    test.destroy()
    return width, height


def set_screen(window_width, window_height):
    global screen
    screen = display.set_mode((window_width, window_height))
    screen.fill((255, 255, 255))


def show_text(screen, text='text box', centreX=0, centreY=0,
              font_colour=(0, 0, 0), font_bg=(255, 255, 255), font_size=10):
    # initialises font for displaying text

    # try:
    # basic_font = pygame.font.SysFont('unifont.ttf', fontSize)
    basic_font = font.Font('Vogue.ttf', font_size)
    # basic_font = pygame.font.Font(None, fontSize)
    text = basic_font.render(text, True, font_colour, font_bg)
    text_rect = text.get_rect()
    text_rect.center = (centreX, centreY)  #
    screen.blit(text, text_rect)  # Shows text on screen


# except:
# pass


def show_image(image, x, y):
    image = py_image.load(fileLocation + image + '.jpg').convert()
    screen.blit(image, (x, y))


def average_of_colour(colour):
    (r, g, b) = (colour[0], colour[1], colour[2])
    avg = int((r + g + b) / 3)
    return 255 - avg, 255 - avg, 255 - avg
