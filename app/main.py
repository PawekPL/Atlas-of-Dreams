import pyglet
from libs.screen_manager import SceneManager
from pyglet.gl import *
from screens.menu import *

if __name__ == '__main__':
    scenemgr = SceneManager("menu", {"menu": Menu()}, show_fps=True)
