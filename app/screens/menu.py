from libs.screen_manager import Scene
import pyglet
from pyglet.gl import *
from libs.widgets import OneTimeButton, updateLabel, set_state
import types
import time


def output():
    print(1)


def new():
    print(2)


class Menu(Scene):
    def __init__(self, window):
        super().__init__()
        glEnable(GL_TEXTURE_2D)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        self.assetpos = [(515/1280, 380/720), (515/1280, 230/720),
                         (515/1280, 80/720), (540/1280, 510/720)]
        self.assetsize = [(250/1280, 120/720), (200/1280, 200/720)]
        self.window = window

        self.pressed = pyglet.image.load("./assets/button-down.png")
        self.depressed = pyglet.image.load("./assets/button.png")
        self.logopng = pyglet.image.load("./assets/logo.png")

        self.batch = pyglet.graphics.Batch()
        self.labelbatch = pyglet.graphics.Batch()
        # Button to create a new project
        self.newbutton = OneTimeButton(self.assetpos[0][0]*self.window.width,
                                       self.assetpos[0][1]*self.window.height,
                                       self.pressed,
                                       self.depressed,
                                       batch=self.batch)


        self.newlabel = pyglet.text.Label("New Project",
                                          font_size=self.newbutton.height//5,
                                          x=self.newbutton.x+self.newbutton.width//2,
                                          y=self.newbutton.y+self.newbutton.height//2,
                                          batch=self.labelbatch,
                                          color=(0, 0, 0, 255),
                                          anchor_x='center',
                                          anchor_y='center')

        # Button to open an existing project
        self.loadbutton = OneTimeButton(self.assetpos[1][0]*self.window.width,
                                        self.assetpos[1][1]*self.window.height,
                                        self.pressed,
                                        self.depressed,
                                        batch=self.batch)

        self.loadbutton.set_handler('on_release', output)


        self.loadlabel = pyglet.text.Label("Load Project",
                                           font_size=self.loadbutton.height//5,
                                           x=self.loadbutton.x+self.loadbutton.width//2,
                                           y=self.loadbutton.y+self.loadbutton.height//2,
                                           batch=self.labelbatch,
                                           color=(0, 0, 0, 255),
                                           anchor_x='center',
                                           anchor_y='center')

        # Button to open settings
        self.settingsbutton = OneTimeButton(self.assetpos[2][0]*self.window.width,
                                            self.assetpos[2][1] *
                                            self.window.height,
                                            self.pressed,
                                            self.depressed,
                                            batch=self.batch)

        self.settingsbutton.set_handler('on_release', output)


        self.settingslabel = pyglet.text.Label("Settings",
                                               font_size=self.settingsbutton.height//5,
                                               x=self.settingsbutton.x+self.settingsbutton.width//2,
                                               y=self.settingsbutton.y+self.settingsbutton.height//2,
                                               batch=self.labelbatch,
                                               color=(0, 0, 0, 255),
                                               anchor_x='center',
                                               anchor_y='center')

        self.logo = pyglet.sprite.Sprite(self.logopng,
                                         self.assetpos[3][0]*self.window.width,
                                         self.assetpos[3][1] *
                                         self.window.height,
                                         batch=self.batch)
        group = self.logo._group
        self.logo._group.set_state = types.MethodType(set_state, group)

        self.buttons = [self.newbutton, self.loadbutton, self.settingsbutton]

    def on_draw(self, manager):
        manager.window.clear()
        pyglet.gl.glClearColor(75/255, 0/255, 0/255, 1)
        super().on_draw(manager)
        self.batch.draw()
        self.labelbatch.draw()

    def on_activate(self, manager):
        pass

    def on_resize(self, manager, w, h):
        self.newbutton.update(x=self.assetpos[0][0]*self.window.width,
                              y=self.assetpos[0][1]*self.window.height,
                              width=self.assetsize[0][0]*self.window.width,
                              height=self.assetsize[0][1]*self.window.height,
                              imgsize=(250, 120),
                              nearest=True)
        self.loadbutton.update(x=self.assetpos[1][0]*self.window.width,
                               y=self.assetpos[1][1]*self.window.height,
                               width=self.assetsize[0][0]*self.window.width,
                               height=self.assetsize[0][1]*self.window.height,
                               imgsize=(250, 120),
                               nearest=True)
        self.settingsbutton.update(x=self.assetpos[2][0]*self.window.width,
                                   y=self.assetpos[2][1]*self.window.height,
                                   width=self.assetsize[0][0] *
                                   self.window.width,
                                   height=self.assetsize[0][1] *
                                   self.window.height,
                                   imgsize=(250, 120),
                                   nearest=True)

        self.logo.update(x=self.assetpos[3][0]*self.window.width,
                         y=self.assetpos[3][1]*self.window.height,
                         scale_x=self.assetsize[1][0]*self.window.width/200,
                         scale_y=self.assetsize[1][1]*self.window.height/200)

        updateLabel(self.newlabel,
                    font_size=self.newbutton.height//5,
                    x=self.newbutton.x+self.newbutton.width//2,
                    y=self.newbutton.y+self.newbutton.height//2)

        updateLabel(self.loadlabel,
                    font_size=self.loadbutton.height//5,
                    x=self.loadbutton.x+self.loadbutton.width//2,
                    y=self.loadbutton.y+self.loadbutton.height//2)

        updateLabel(self.settingslabel,
                    font_size=self.settingsbutton.height//5,
                    x=self.settingsbutton.x+self.settingsbutton.width//2,
                    y=self.settingsbutton.y+self.settingsbutton.height//2)

    def on_mouse_press(self, manager, x, y, buttons, modifiers):

        self.newbutton.on_mouse_press(x, y, buttons, modifiers)
        self.loadbutton.on_mouse_press(x, y, buttons, modifiers)
        self.settingsbutton.on_mouse_press(x, y, buttons, modifiers)
        
        if self.newbutton.value:
            self.window.current = "new"
            if not self.newbutton.nearest:
                self.newbutton.update(nearest=True)
                self.newbutton.nearest = True

        elif self.loadbutton.value:
            if not self.loadbutton.nearest:
                self.loadbutton.update(nearest=True)
                self.loadbutton.nearest = True

        elif self.settingsbutton.value:
            if not self.settingsbutton.nearest:
                self.settingsbutton.update(nearest=True)
                self.settingsbutton.nearest = True

    def on_mouse_release(self, manager, x, y, buttons, modifiers):
        self.newbutton.on_mouse_release(x, y, buttons, modifiers)
        self.loadbutton.on_mouse_release(x, y, buttons, modifiers)
        self.settingsbutton.on_mouse_release(x, y, buttons, modifiers)
