import tkinter as tk
import pygame
import sys
import pickle
import os
from Project import Project
from utils import APP_PATH


class App:
    def __init__(self, project):
        self.project = project
        project.app = self
        self.running = True
        self.events = None
        pygame.display.set_caption('Animatis - ' + project.name)

    def check_events(self):
        self.events = pygame.event.get()
        for event in self.events:

            if event.type == pygame.QUIT:
                self.save_project()

                with open(APP_PATH, 'wb') as file:
                    self.events = []
                    pickle.dump(self, file)

                pygame.quit()
                sys.exit()

            keys = pygame.key.get_pressed()
            if keys[pygame.K_LCTRL]:
                if keys[pygame.K_s]:
                    self.save_as_window()
                elif keys[pygame.K_o]:
                    self.open_window()
                elif keys[pygame.K_n]:
                    self.new_project()

    def save_project(self):
        file = open(self.project.name, 'wb')
        self.project.app = None
        pickle.dump(self.project.get_data(), file)
        self.project.app = self

    def save_as_window(self):
        root = tk.Tk()
        root.title('Save as')
        root.attributes('-topmost', True)
        root.geometry('500x100')

        name = tk.Entry(root, width=15, font='Calibri 20')
        name.place(relx=0.0, rely=0.0)
        name.bind('<Return>', lambda event: self.save_as(name.get(), root))
        root.after(1, lambda: name.focus_force())
        name.insert(0, self.project.name)

        root.mainloop()

    def save_as(self, name, window):
        if os.path.exists(self.project.name):
            os.remove(self.project.name)
        os.makedirs(os.path.dirname(name), exist_ok=True)
        self.project.name = name
        self.save_project()
        window.destroy()

    def open_window(self):
        root = tk.Tk()
        root.title('Open')
        root.attributes('-topmost', True)
        root.geometry('500x100')

        name = tk.Entry(root, width=15, font='Calibri 20')
        name.place(relx=0.0, rely=0.0)
        name.bind('<Return>', lambda event: self.open(name.get(), root))
        root.after(1, lambda: name.focus_force())
        name.insert(0, self.project.name)

        root.mainloop()

    def open(self, name, window):
        self.save_project()
        pygame.display.set_caption('Animatis - ' + name)
        file = open(name, 'rb')
        self.project = pickle.load(file).get_project()
        self.project.app = self
        self.project.initialise()
        window.destroy()

    def main(self):
        self.project.initialise()
        while self.running:
            self.check_events()
            self.project.main()
            pygame.display.update()

    def new_project(self):
        self.save_project()
        self.project = Project(self.project.window_width,
                               self.project.window_height,
                               'untitled', app=self)
