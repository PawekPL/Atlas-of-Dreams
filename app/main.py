import os
if os.getcwd()[-4:] != "\\app":  # To run straight in Atom without file not found errors
    print(os.getcwd())
    os.chdir(f"{os.getcwd()}\\app")
    

from screens.worldgeneration import WorldGen
import pyglet
from libs.screen_manager import SceneManager, Scene
from pyglet.gl import *
from screens.menu import Menu
from screens.newproject import NewProject

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
        self.scenes = {
            "menu": Menu(self.window),
            "new": NewProject(self.window),
            "gen": WorldGen(self.window)
        }

        self.current = "gen"
        self.window.current = "gen"

        @self.window.event
        def on_mouse_release(_, __, ___, ____):
            if self.window.current != self.current:
                self.current = self.window.current
                self.scenes[self.current].on_resize(self, None, None)


class Empty(Scene):
    """Empty scene for initialisation"""

    def __init__(self):
        super().__init__()

    def on_draw(self, manager):
        super().on_draw(manager)
        manager.window.clear()


if __name__ == '__main__':

    scenemgr = Manager(resolution=(
        1280, 720), title="Atlas Of Dreams", show_fps=False, vsync=False, fps=10000)
    pyglet.app.run()

