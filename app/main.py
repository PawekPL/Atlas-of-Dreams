import pyglet
from libs.screen_manager import SceneManager
from pyglet.gl import *
from screens.menu import Menu


if __name__ == '__main__':
    scenes = {}
    scenes["menu"] = Menu()
    scenemgr = SceneManager("menu", scenes,(1280,720),"Atlas Of Dreams", show_fps=True,vsync=False)
