import types  # Source: https://groups.google.com/g/pyglet-users/c/s8Icda9oPnY
from libs.screen_manager import Scene
import pyglet
from pyglet.gl import *
from pyglet.gui import *
from libs.widgets import OneTimeButton, updateLabel, ToggleButton

import time


def output():
    print(time.time())


def set_state(self):
    glEnable(self.texture.target)
    glBindTexture(self.texture.target, self.texture.id)
    glPushAttrib(GL_COLOR_BUFFER_BIT)
    glEnable(GL_BLEND)
    glTexParameteri(self.texture.target, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    glBlendFunc(self.blend_src, self.blend_dest)


class NewProject(Scene):
    def __init__(self, window):
        super().__init__()

        self.window = window
        self.window.params = {"name": "New Project",
                              "seed": 0,
                              "gen_structures": True,
                              }

        self.batch = pyglet.graphics.Batch()
        self.labelbatch = pyglet.graphics.Batch()
        

    def on_draw(self, manager):
        super().on_draw(manager)
        manager.window.clear()
        pyglet.gl.glClearColor(75/255, 0/255, 0/255, 1)
        self.batch.draw()
        self.labelbatch.draw()

    def on_activate(self, manager):
        pass

    def on_resize(self, manager, w, h):
        pass

    def on_mouse_press(self, manager, x, y, buttons, modifiers):
        pass

    def on_mouse_release(self, manager, x, y, buttons, modifiers):
        pass
