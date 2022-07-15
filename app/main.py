import os

if os.getcwd()[-4:] != "\\app":  # To run straight in IDE without file not found errors
    print(os.getcwd())
    os.chdir(f"{os.getcwd()}\\app")


import json

import pyglet
from pyglet.gl import *

from libs.screen_manager import Scene, SceneManager
from screens.menu import Menu
from screens.newproject import NewProject
from screens.view2d import View2D
from screens.view3d import View3D
from screens.worldgeneration import WorldGen
from screens.loadproject import LoadProject
from screens.settings import Settings


class Manager(SceneManager):

    def __init__(self, resolution, title="Untitled", fps=10000, show_fps=False, vsync=False, resizable=True):
        super().__init__(start="",
                         scenes={"": Empty()},
                         resolution=resolution,
                         title=title,
                         fps=fps,
                         show_fps=show_fps,
                         vsync=vsync,
                         resizable=resizable)
        self.window.set_minimum_size(120, 50)
        self.window.WORLD_PROPERTIES = {}
        self.scenes = {
            "menu": Menu(self,self.window),
            "new": NewProject(self,self.window),
            "gen": WorldGen(self.window),
            "3Dview": View3D(self,self.window),
            "2Dview": View2D(self,self.window),
            "load": LoadProject(self,self.window),
            "settings": Settings(self,self.window)
        }
        self.current = "menu"
        self.previous = ""

    def set_scene(self, scene):
        self.scenes[scene].on_resize(self, 
                                     self.window.width, 
                                     self.window.height)
        try:
            self.scenes[scene].on_load()
        except Exception as e:
            print(e)
        self.current = scene


    def on_step(self, dt):        
        super().on_step(dt)


class Empty(Scene):
    """Empty scene for initialisation"""

    def __init__(self):
        super().__init__()

    def on_draw(self, manager):
        super().on_draw(manager)
        manager.window.clear()


if __name__ == '__main__':
    settings = json.load(open("config/settings.json"))
    scenemgr = Manager(
        resolution=settings["resolution"], 
        title="Atlas Of Dreams", 
        show_fps=settings["show_fps"], 
        vsync=settings["vsync"], 
        fps=settings["fps_limit"])
    pyglet.app.run()
