
import os

import pyglet
from libs.screen_manager import Scene
from libs.widgets import OneTimeButton, updateLabel
from pyglet.gl import *
from pyglet.gui import *


class LoadProject(Scene):
    def __init__(self, manager, window):
        
        super().__init__()
        self.manager = manager
        #assrt positions and sizes
        self.assetpos = [(40/1280, 640/720), (990/1280, 640/720),
                         (515/1280, 80/720), (540/1280, 510/720)]
        self.assetsize = [(250/1280, 60/720), (200/1280, 200/720)]
        #context
        self.window = window
        #load button images
        self.pressed = pyglet.image.load("./assets/button-down.png")
        self.depressed = pyglet.image.load("./assets/button.png")
        #create batches
        self.batch = pyglet.graphics.Batch()
        self.labelbatch = pyglet.graphics.Batch()

        # Button to go back to the main menu
        self.backbutton = OneTimeButton(
            self.assetpos[0][0]*self.window.width,
            self.assetpos[0][1]*self.window.height,
            self.pressed,
            self.depressed,
            batch=self.batch)

        self.backbutton.set_handler('on_release', self.back)

        self.backlabel = pyglet.text.Label(
            "Back",
            font_size=self.backbutton.height//5,
            x=self.backbutton.x+self.backbutton.width//2,
            y=self.backbutton.y+self.backbutton.height//2,
            batch=self.labelbatch,
            color=(0, 0, 0, 255),
            anchor_x='center',
            anchor_y='center')

        # Button to go to the next scene
        self.startbutton = OneTimeButton(
            self.assetpos[1][0]*self.window.width,
            self.assetpos[1][1] *
            self.window.height,
            self.pressed,
            self.depressed,
            batch=self.batch)

        self.startbutton.set_handler('on_release', self.next)

        self.startlabel = pyglet.text.Label(
            "Start",
            font_size=self.startbutton.height//5,
            x=self.startbutton.x+self.startbutton.width//2,
            y=self.startbutton.y+self.startbutton.height//2,
            batch=self.labelbatch,
            color=(0, 0, 0, 255),
            anchor_x='center',
            anchor_y='center')
        #Input box for the name of the project
        self.nameinput = TextEntry(
            "Project Name",
            self.window.width//2,
            4*self.window.height//5,
            self.window.width//4,
            batch=self.batch)
        self.nameinput.set_handler('on_commit', self.name_update)

        self.namelabel = pyglet.text.Label(
            text="Project Name:",
            x=3*self.window.width//8,
            y=41*self.window.height//50,
            font_size=self.window.height//25,
            batch=self.labelbatch,
            color=(200, 200, 5, 255),
            anchor_x='center',
            anchor_y='center')

    def on_draw(self, manager):
        
        super().on_draw(manager)
        #clear the screen
        manager.window.clear()
        pyglet.gl.glClearColor(75/255, 0/255, 0/255, 1)
        #draw the batches
        self.batch.draw()
        self.labelbatch.draw()

    def on_activate(self, manager):
        pass

    def on_resize(self, manager, w, h):
        """When the window is resized, update the buttons' and labels' positions"""
        self.backbutton.update(
            x=self.assetpos[0][0]*self.window.width,
            y=self.assetpos[0][1]*self.window.height,
            width=self.assetsize[0][0]*self.window.width,
            height=self.assetsize[0][1]*self.window.height,
            imgsize=(250, 120),
            nearest=True)
        self.startbutton.update(
            x=self.assetpos[1][0]*self.window.width,
            y=self.assetpos[1][1]*self.window.height,
            width=self.assetsize[0][0]*self.window.width,
            height=self.assetsize[0][1]*self.window.height,
            imgsize=(250, 120),
            nearest=True)

        updateLabel(
            self.backlabel,
            font_size=self.backbutton.height//5,
            x=self.backbutton.x+self.backbutton.width//2,
            y=self.backbutton.y+self.backbutton.height//2)

        updateLabel(
            self.startlabel,
            font_size=self.startbutton.height//5,
            x=self.startbutton.x+self.startbutton.width//2,
            y=self.startbutton.y+self.startbutton.height//2)

        self.nameinput._x = w//2
        self.nameinput._y = 4*h//5
        self.nameinput._width = w//4
        self.nameinput._update_position()

        updateLabel(
            self.namelabel,
            x=3*self.window.width//8,
            y=41*self.window.height//50,
            font_size=self.window.height//25)

    def on_text(self, manager, text):
        self.nameinput.on_text(text)

    def on_text_motion(self, app, motion):
        self.nameinput.on_text_motion(motion)

    def on_text_motion_select(self, app, motion):
        self.nameinput.on_text_motion_select(motion)

    def on_mouse_press(self, manager, x, y, buttons, modifiers):
        """When the mouse is pressed, check if the buttons are pressed"""
        self.backbutton.on_mouse_press(x, y, buttons, modifiers)
        self.startbutton.on_mouse_press(x, y, buttons, modifiers)
        self.nameinput.on_mouse_press(x, y, buttons, modifiers)

        if self.backbutton.value:
            if not self.backbutton.nearest:
                self.backbutton.update(nearest=True)
                self.backbutton.nearest = True

        elif self.startbutton.value:
            if not self.startbutton.nearest:
                self.startbutton.update(nearest=True)
                self.startbutton.nearest = True

    def on_mouse_release(self, manager, x, y, buttons, modifiers):
        """When the mouse is released, check if the buttons are depressed"""
        self.backbutton.on_mouse_release(x, y, buttons, modifiers)
        self.startbutton.on_mouse_release(x, y, buttons, modifiers)

    def name_update(self, val):
        """Check the name from the Text Input"""
        val = val.replace("<", "")
        val = val.replace(">", "")
        val = val.replace("/", "")
        val = val.replace("\\", "")
        val = val.replace(":", "")
        val = val.replace("\"", "")
        val = val.replace("|", "")
        val = val.replace("?", "")
        val = val.replace("*", "")
        val = val.replace(".", "")
        if not os.path.exists("saves/"+val):
            val = self.nameinput.value
            
        self.nameinput.value = val

    def back(self):
        self.manager.set_scene("menu")

    def next(self):
        self.window.WORLD_PROPERTIES["name"] = self.nameinput.value
        self.window.WORLD_PROPERTIES["path"] = "saves/"+self.nameinput.value
        self.manager.set_scene("2Dview")
