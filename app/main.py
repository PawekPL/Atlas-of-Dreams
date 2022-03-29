import pyglet
from libs.screen_manager import SceneManager,Scene
from pyglet.gl import *
from screens.menu import Menu
import os

class Manager(SceneManager):

    def __init__(self, resolution, title="Untitled", fps=-1, show_fps=False,vsync=False,resizable=True):
        super().__init__(start="",
                         scenes={"":Empty()},
                         resolution=resolution,
                         title=title,
                         fps=fps,
                         show_fps=show_fps,
                         vsync=vsync,
                         resizable=resizable)
        print(1)
        self.scenes = {
                       "menu":Menu(self.window)
        }
        self.current = "menu"

class Empty(Scene):
    """Empty scene for initialisation"""
    def __init__(self):
        super().__init__()

    def on_draw(self, manager):
        super().on_draw(manager)
        manager.window.clear()



if __name__ == '__main__':
    if os.getcwd()[-4:] != "\\app": # To run straight in Atom without file not found errors
        print(os.getcwd())
        os.chdir(f"{os.getcwd()}\\app")
    scenemgr = Manager(resolution=(1280,720),title="Atlas Of Dreams", show_fps=True,vsync=False,fps=-1)
    pyglet.app.run()
