# -*- coding: utf-8 -*-
"""
Created on Sun Jun 21 19:38:03 2020

@author: rohan
"""
from Frame import Frame
from Stroke import Stroke
from Colour_Panel import ColourPanel
from pygame import event as events
from pygame import (quit, init, font, mouse, key, QUIT, MOUSEBUTTONDOWN,
                    MOUSEMOTION, MOUSEBUTTONUP, KEYDOWN, K_UP, K_DOWN,
                    K_LEFT, K_RIGHT, K_LCTRL, K_v, K_p, display, K_SPACE,
                    K_MINUS, K_EQUALS, K_m, K_x, K_c, K_b,
                    K_z, K_f, K_l, K_d, K_o, K_BACKSPACE, K_u, K_s, K_e)
from sys import exit as sys_exit
import utils
from src.Tool import Tool
from utils import show_text
from copy import deepcopy
from time import sleep
from math import hypot

init()
font.init()


class Project:
    def __init__(self, window_width, window_height, name='my_animation',
                 frames=None, app=None):
        self.name = name
        self.window_width, self.window_height = window_width, window_height
        self.frames = frames
        if frames is None:
            self.frames = [Frame(self)]
        self.current_frame = 0
        self.down = False
        self.tool_width = 2
        self.update = False
        self.onion_skin = True
        self.colour = (0, 0, 0)
        self.radius = 15
        self.fps = 10  # Frame rate
        self.play = False
        self.selected_frames = []
        self.copied_frames = []
        self.cut = False
        self.tool = Tool.PEN
        self.current_stroke = Stroke(self.tool_width, self.colour, self)
        self.colour_panel = ColourPanel(900, 10, 100, 100, 2,
                                        self.generate_colours(), self)
        self.active = False  # User drawing something
        self.clear_screen = False  # Erase and redraw screen
        self.marking = False
        self.mark_frame = Frame(self)
        self.app = app

        self.initialise()

    def initialise(self):
        self.get_screen().fill((255, 255, 255))
        self.show_info()
        self.colour_panel.show()
        self.show_onion_skin()
        self.get_current_frame().show(colour=None, show_border=True)

    def get_screen(self):
        return utils.screen

    def main(self):
        self.check_events()
        self.update_colour_panel()
        self.show()

    def update_colour_panel(self):
        if self.colour_panel.move:
            self.colour_panel.set_cor(mouse.get_pos())
            self.colour_panel.set_positions()
            self.update_screen()

    def update_screen(self):
        self.clear_screen = True

    def generate_colours(self):
        colours = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (0, 0, 0),
                   (255, 255, 255), (255, 255, 0)]

        return colours

    def get_current_frame(self):
        if self.marking:
            return self.mark_frame

        return self.frames[self.current_frame]

    def check_events(self):
        for event in self.app.events:
            if event.type == MOUSEBUTTONDOWN:
                self.active = True

                if event.button == 1:
                    self.down = True

                    if self.colour_panel.is_mouse_over():
                        self.colour = self.colour_panel.get_selected_colour()

                    elif self.tool == Tool.PEN:
                        self.current_stroke.add_point(mouse.get_pos())

                elif event.button == 3:
                    if self.colour_panel.is_mouse_over():
                        self.colour_panel.move = True
                        self.update_screen()

            elif event.type == MOUSEMOTION:
                if self.down:
                    if self.tool == Tool.PEN:
                        self.current_stroke.add_point(mouse.get_pos())

                    elif self.tool == Tool.STROKE_ERASER:
                        self.erase_stroke()

                    elif self.tool == Tool.ERASER:
                        self.erase_points()

            elif event.type == MOUSEBUTTONUP:
                self.active = False

                if event.button == 1:
                    self.down = False
                    self.get_current_frame().add_stroke(self.current_stroke)
                    self.current_stroke = Stroke(self.tool_width, self.colour,
                                                 self)

                elif event.button == 3:
                    if self.colour_panel.is_mouse_over():
                        self.colour_panel.move = False

            elif event.type == KEYDOWN:
                keys_pressed = key.get_pressed()

                for i in ([i for i in range(97, 123)]
                          + [K_UP, K_DOWN, K_LEFT, K_RIGHT,
                             K_LCTRL, K_BACKSPACE]):
                    if keys_pressed[i]:
                        self.clear_screen = self.active = True

                # Add new frame
                if keys_pressed[K_f]:
                    self.current_frame += 1
                    self.insert_frame(self.current_frame, Frame(self))

                    # Add new layer
                elif keys_pressed[K_l]:
                    self.get_current_frame().add_layer()
                # Toggle onion skin
                elif keys_pressed[K_o]:
                    self.onion_skin = not self.onion_skin
                # Select/unselect current frame
                elif (keys_pressed[K_s]
                      and not keys_pressed[K_LCTRL]):
                    frame = self.get_current_frame()

                    if frame.selected:
                        frame.unselect()

                    else:
                        frame.select()
                        self.selected_frames.append(frame)
                # unselect
                elif keys_pressed[K_u]:
                    for frame in self.frames:
                        frame.unselect()
                # Delete current frame
                elif keys_pressed[K_BACKSPACE]:
                    if len(self.frames) > 1:
                        frame = self.get_current_frame()
                        self.frames.remove(frame)

                        try:
                            self.selected_frames.remove(frame)
                        except:
                            pass

                        try:
                            self.copied_frames.remove(frame)
                        except:
                            pass

                        if len(self.frames) == 0:
                            self.frames = [Frame(self)]
                        else:
                            self.current_frame = min(self.current_frame,
                                                     len(self.frames) - 1)

                # Delete current layer
                elif keys_pressed[K_d]:
                    frame = self.get_current_frame()
                    if len(frame.layers) > 1:
                        frame.layers.remove(frame.get_current_layer())
                    frame.current_layer = min(frame.current_layer,
                                              len(frame.layers) - 1)
                # Previous frame
                elif keys_pressed[K_LEFT]:
                    self.prev_frame()
                # Next frame
                elif keys_pressed[K_RIGHT]:
                    self.next_frame()
                # Layer above
                elif keys_pressed[K_UP]:
                    self.get_current_frame().next_layer()
                # Layer below
                elif keys_pressed[K_DOWN]:
                    self.get_current_frame().prev_layer()
                # Undo
                elif (keys_pressed[K_LCTRL]
                      and keys_pressed[K_z]):
                    self.get_current_frame().undo()
                # Copy selected frames
                elif (keys_pressed[K_LCTRL]
                      and keys_pressed[K_c]):
                    self.copy_frames()
                # Paste frames
                elif (keys_pressed[K_LCTRL]
                      and keys_pressed[K_v]):
                    self.paste_frames(self.current_frame + 1)
                # Cut frames
                elif (keys_pressed[K_LCTRL]
                      and keys_pressed[K_x]):
                    self.cut_frames()
                # Save 
                elif (keys_pressed[K_LCTRL]
                      and keys_pressed[K_s]):
                    self.save()

                # Select PEN
                elif keys_pressed[K_p]:
                    self.tool = Tool.PEN

                # Select ERASER
                elif keys_pressed[K_e]:
                    if self.tool == Tool.PEN or self.tool == Tool.ERASER:
                        self.tool = Tool.STROKE_ERASER
                    elif self.tool == Tool.STROKE_ERASER:
                        self.tool = Tool.ERASER

                # Increase size of tool
                elif keys_pressed[K_EQUALS]:
                    self.tool_width += 1
                # Decrease size of tool
                elif keys_pressed[K_MINUS]:
                    self.tool_width = max(0, self.tool_width - 1)

                elif keys_pressed[K_m]:
                    self.marking = not self.marking

                elif keys_pressed[K_b]:
                    current_frame = self.get_current_frame()
                    if current_frame.is_background:
                        current_frame.set_background(False)
                    else:
                        current_frame.set_background(True)

        if key.get_pressed()[K_SPACE]:
            self.play_animation(self.current_frame)

    def insert_frame(self, index, frame):
        self.frames.insert(index, frame)

    def cut_frames(self):
        if len(self.copied_frames) < len(self.frames):
            self.copy_frames()

            for frame in self.selected_frames:
                self.frames.remove(frame)

            self.current_frame = min(self.current_frame,
                                     len(self.frames) - 1)
            self.selected_frames = []
            self.cut = True

    def paste_frames(self, index):
        for frame in self.copied_frames:
            print(index, frame)
            self.frames.insert(index, deepcopy(frame))
            index += 1

        if self.cut:
            self.copied_frames = []
            self.cut = False

    def copy_frames(self):
        self.copied_frames = self.selected_frames.copy()

    def prev_frame(self):
        self.current_frame = self.current_frame - 1

        if self.current_frame == -1:
            self.current_frame = len(self.frames) - 1

    def next_frame(self):
        self.current_frame = (self.current_frame + 1) % len(self.frames)

    def show_onion_skin(self):
        self.show_background_frame()
        if self.current_frame > 1:
            frame = self.frames[self.current_frame - 2]
            frame.show((230, 230, 255), False)

        if self.current_frame > 0:
            frame = self.frames[self.current_frame - 1]
            frame.show((255, 180, 180), False)

        if self.current_frame < len(self.frames) - 1:
            frame = self.frames[self.current_frame + 1]
            frame.show((180, 255, 180), False)

    def play_animation(self, start):
        background = None
        for i in range(start, len(self.frames)):
            self.get_screen().fill((255, 255, 255))
            frame = self.frames[i]
            frame.show()

            if background is not None:
                background.show()

            display.update()

            if frame.is_background:
                background = frame

            if not key.get_pressed()[K_SPACE]:
                return

            sleep(1 / self.fps)

        self.update_screen()

    def show_info(self):
        frame = self.get_current_frame()
        start_x = 150
        start_y = 30
        if self.marking:
            text = 'Marking mode'
        else:
            text = ''
            if frame.is_background:
                start_x += 50
                text += 'Background '
            text += 'Frame ' + str(self.current_frame + 1) + ' of '
            text += str(len(self.frames))

        show_text(self.get_screen(), text, start_x, start_y, font_size=30)

        if self.marking:
            pass
        else:

            text = 'Layer ' + str(frame.current_layer + 1) + ' of '
            text += str(len(frame.layers))
            show_text(self.get_screen(), text, start_x, start_y + 30, font_size=30)

        if self.tool == Tool.PEN:
            text = 'Pen'
        elif self.tool == Tool.ERASER:
            text = 'Eraser'
        elif self.tool == Tool.STROKE_ERASER:
            text = 'Stroke Eraser'

        text += ' of radius ' + str(self.tool_width)

        show_text(self.get_screen(), text, start_x, start_y + 70, font_size=30)

    def undo(self):
        self.get_current_frame().undo()

    def save(self):
        import pickle

        with open(self.name, 'wb') as file:
            pickle.dump(self, file)

    def show(self):
        if self.active:
            if self.clear_screen:
                # Redraw current frame
                self.get_screen().fill((255, 255, 255))
                if self.onion_skin:
                    self.show_onion_skin()

                if self.marking:
                    self.frames[self.current_frame].show()

                self.get_current_frame().show(colour=None,
                                              show_border=True)

            # Draw current stroke
            self.current_stroke.draw(colour=self.colour)

        if self.clear_screen:
            # Show information
            self.show_info()
            self.colour_panel.show()

        # Always show markings
        self.mark_frame.show()
        # Reset value
        self.clear_screen = False

    def erase_stroke(self):
        x, y = mouse.get_pos()
        layer = self.get_current_frame().get_current_layer()
        strokes = layer.get_strokes()
        found = False
        for i in range(len(strokes) - 1):
            stroke = strokes[i]
            points = stroke.get_points()
            for j in range(len(points) - 1):
                (x1, y1) = points[j]
                (x2, y2) = points[j + 1]
                grad1 = (y2 - y1) / max((x2 - x1), 0.1)
                grad2 = (y2 - y) / max((x2 - x), 0.1)
                if (abs(grad2 - grad1) < 0.1
                        and min(x1, x2) <= x <= max(x1, x2)
                        and min(y1, y2) <= y <= max(y1, y2)):
                    self.update_screen()
                    found = True
                    strokes.remove(stroke)
                    break
            if found:
                break

    def erase_points(self):
        x, y = mouse.get_pos()
        layer = self.get_current_frame().get_current_layer()
        strokes = layer.get_strokes()
        for stroke in strokes:
            points = stroke.get_points()
            strokes.remove(stroke)
            partitions = []
            temp_points = []
            # Find all points that need to be erased
            for (a, b) in points:
                if hypot(x - a, y - b) < 5 * self.tool_width:
                    self.update_screen()
                    partitions.append(temp_points)
                    temp_points = []
                else:
                    temp_points.append((a, b))
                # Add remaining points
            if temp_points:
                partitions.append(temp_points)

            # For each section of original stroke create a new stroke
            # and add it to the layer
            for points in partitions:
                new_stroke = Stroke(stroke.width, stroke.colour,
                                    stroke.app, points=points)
                strokes.append(new_stroke)

    def show_background_frame(self):
        i = self.current_frame
        while i >= 1:
            i -= 1
            curr = self.frames[i]
            if curr.is_background:
                curr.show()
                return

    def get_data(self):
        data = ProjectData()
        data.name = self.name
        data.window_width = self.window_width
        data.window_height = self.window_height
        data.frames = self.frames
        data.current_frame = self.current_frame
        data.down = self.down
        data.tool_width = self.tool_width
        data.update = self.update
        data.onion_skin = self.onion_skin
        data.colour = self.colour
        data.radius = self.radius
        data.fps = self.fps  # Frame rate
        data.play = self.play
        data.selected_frames = self.selected_frames
        data.copied_frames = self.copied_frames
        data.cut = self.cut
        data.tool = self.tool
        data.current_stroke = self.current_stroke
        data.colour_panel = self.colour_panel
        data.active = self.active  # User drawing something
        data.clear_screen = self.clear_screen  # Erase and redraw screen
        data.marking = self.marking
        data.mark_frame = self.mark_frame

        return data


class ProjectData:
    def __init__(self):
        pass

    def get_project(self):
        project = Project(self.window_width, self.window_height, self.name)

        project.name = self.name
        project.window_width = self.window_width
        project.window_height = self.window_height
        project.frames = self.frames
        project.current_frame = self.current_frame
        project.down = self.down
        project.tool_width = self.tool_width
        project.update = self.update
        project.onion_skin = self.onion_skin
        project.colour = self.colour
        project.radius = self.radius
        project.fps = self.fps  # Frame rate
        project.play = self.play
        project.selected_frames = self.selected_frames
        project.copied_frames = self.copied_frames
        project.cut = self.cut
        project.tool = self.tool
        project.current_stroke = self.current_stroke
        project.colour_panel = self.colour_panel
        project.active = self.active  # User drawing something
        project.clear_screen = self.clear_screen  # Erase and redraw screen
        project.marking = self.marking
        project.mark_frame = self.mark_frame

        return project
