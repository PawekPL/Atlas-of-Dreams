import time

import pyglet
from libs.screen_manager import Scene
from libs.widgets import OneTimeButton, updateLabel
from pyglet.gl import *
from pyglet.gui import *


def output():
    print(time.time())



class NewProject(Scene):
    def __init__(self,manager, window):
        super().__init__()
    
        self.manager = manager
        #asset positions and sizes
        self.assetpos = [(40/1280, 640/720), (990/1280, 640/720),
                         (515/1280, 80/720), (540/1280, 510/720)]
        self.assetsize = [(250/1280, 60/720), (200/1280, 200/720)]
        
        self.window = window
        #load assets
        self.pressed = pyglet.image.load("./assets/button-down.png")
        self.depressed = pyglet.image.load("./assets/button.png")
        #declare batches
        self.batch = pyglet.graphics.Batch()
        self.labelbatch = pyglet.graphics.Batch()
        

        # Button to go back to the main menu
        self.backbutton = OneTimeButton(self.assetpos[0][0]*self.window.width,
                                        self.assetpos[0][1]*self.window.height,
                                        self.pressed,
                                        self.depressed,
                                        batch=self.batch)

        self.backbutton.set_handler('on_release', self.back)

        self.backlabel = pyglet.text.Label("Back",
                                           font_size=self.backbutton.height//5,
                                           x=self.backbutton.x+self.backbutton.width//2,
                                           y=self.backbutton.y+self.backbutton.height//2,
                                           batch=self.labelbatch,
                                           color=(0, 0, 0, 255),
                                           anchor_x='center',
                                           anchor_y='center')

        # Button to go to the next scene
        self.startbutton = OneTimeButton(self.assetpos[1][0]*self.window.width,
                                         self.assetpos[1][1] *
                                         self.window.height,
                                         self.pressed,
                                         self.depressed,
                                         batch=self.batch)

        self.startbutton.set_handler('on_release', self.next)

        self.startlabel = pyglet.text.Label("Start",
                                            font_size=self.startbutton.height//5,
                                            x=self.startbutton.x+self.startbutton.width//2,
                                            y=self.startbutton.y+self.startbutton.height//2,
                                            batch=self.labelbatch,
                                            color=(0, 0, 0, 255),
                                            anchor_x='center',
                                            anchor_y='center')
        # Text input for the name of the project
        self.nameinput = TextEntry("Project Name",
                                   self.window.width//2,
                                   4*self.window.height//5,
                                   self.window.width//4,
                                   batch=self.batch)
        self.nameinput.set_handler('on_commit', self.name_update)
        # Text input for the seed of the project
        self.seedinput = TextEntry(str(int(time.time())),
                                   self.window.width//2,
                                   18*self.window.height//25,
                                   self.window.width//4,
                                   batch=self.batch)
        self.seedinput.set_handler('on_commit', self.seed_update)
        # Text input for the size of the project
        self.sizeinput = TextEntry("10",
                                   self.window.width//2,
                                   16*self.window.height//25,
                                   self.window.width//4,
                                   batch=self.batch)
        self.sizeinput.set_handler('on_commit', self.size_update)
        #labels for text boxes
        self.namelabel = pyglet.text.Label(
                                    text="Project Name:",
                                    x=3*self.window.width//8,
                                    y=41*self.window.height//50,
                                    font_size=self.window.height//25,
                                    batch=self.labelbatch,
                                    color=(200, 200, 5, 255),
                                    anchor_x='center',
                                    anchor_y='center')

        self.seedlabel = pyglet.text.Label(
                                    text="Seed:",
                                    x=3*self.window.width//8,
                                    y=37*self.window.height//50,
                                    font_size=self.window.height//25,
                                    batch=self.labelbatch,
                                    color=(200, 200, 5, 255),
                                    anchor_x='center',
                                    anchor_y='center')

        self.sizelabel = pyglet.text.Label(
                                    text="Size:",
                                    x=3*self.window.width//8,
                                    y=33*self.window.height//50,
                                    font_size=self.window.height//25,
                                    batch=self.labelbatch,
                                    color=(200, 200, 5, 255),
                                    anchor_x='center',
                                    anchor_y='center')

        
                                           
                                           

    def on_draw(self, manager):
        super().on_draw(manager)
        manager.window.clear()
        pyglet.gl.glClearColor(75/255, 0/255, 0/255, 1)
        self.batch.draw()
        self.labelbatch.draw()

    def on_activate(self, manager):
        pass

    def on_resize(self, manager, w, h):
        """Update button, label, and Text Box positions on resize"""
        self.backbutton.update(x=self.assetpos[0][0]*self.window.width,
                               y=self.assetpos[0][1]*self.window.height,
                               width=self.assetsize[0][0]*self.window.width,
                               height=self.assetsize[0][1]*self.window.height,
                               imgsize=(250, 120),
                               nearest=True)
        self.startbutton.update(x=self.assetpos[1][0]*self.window.width,
                                y=self.assetpos[1][1]*self.window.height,
                                width=self.assetsize[0][0]*self.window.width,
                                height=self.assetsize[0][1]*self.window.height,
                                imgsize=(250, 120),
                                nearest=True)

        updateLabel(self.backlabel,
                    font_size=self.backbutton.height//5,
                    x=self.backbutton.x+self.backbutton.width//2,
                    y=self.backbutton.y+self.backbutton.height//2)

        updateLabel(self.startlabel,
                    font_size=self.startbutton.height//5,
                    x=self.startbutton.x+self.startbutton.width//2,
                    y=self.startbutton.y+self.startbutton.height//2)

        self.nameinput._x = w//2
        self.nameinput._y = 4*h//5
        self.nameinput._width = w//4
        self.nameinput._update_position()

        self.seedinput._x = w//2
        self.seedinput._y = 18*h//25
        self.seedinput._width = w//4
        self.seedinput._update_position()

        self.sizeinput._x = w//2
        self.sizeinput._y = 16*h//25
        self.sizeinput._width = w//4
        self.sizeinput._update_position()

        updateLabel(self.namelabel,
                    x=3*self.window.width//8,
                    y=41*self.window.height//50,
                    font_size=self.window.height//25)

        updateLabel(self.seedlabel,
                    x=3*self.window.width//8,
                    y=37*self.window.height//50,
                    font_size=self.window.height//25)

        updateLabel(self.sizelabel,
                    x=3*self.window.width//8,
                    y=33*self.window.height//50,
                    font_size=self.window.height//25)

    def on_text(self,manager,text):
        """Handle text input"""
        self.nameinput.on_text(text)
        self.seedinput.on_text(text)
        self.sizeinput.on_text(text)

    def on_text_motion(self, app, motion):
        """Handle text motion"""
        self.nameinput.on_text_motion(motion)
        self.seedinput.on_text_motion(motion)
        self.sizeinput.on_text_motion(motion)

    def on_text_motion_select(self, app, motion):
        """Handle text motion select"""
        self.nameinput.on_text_motion_select(motion)
        self.seedinput.on_text_motion_select(motion)
        self.sizeinput.on_text_motion_select(motion)
        

    def on_mouse_press(self, manager, x, y, buttons, modifiers):
        """Handle mouse press"""
        self.backbutton.on_mouse_press(x, y, buttons, modifiers)
        self.startbutton.on_mouse_press(x, y, buttons, modifiers)
        self.nameinput.on_mouse_press(x, y, buttons, modifiers)
        self.seedinput.on_mouse_press(x, y, buttons, modifiers)
        self.sizeinput.on_mouse_press(x, y, buttons, modifiers)
        

        if self.backbutton.value:
            if not self.backbutton.nearest:
                self.backbutton.update(nearest=True)
                self.backbutton.nearest = True

        elif self.startbutton.value:
            if not self.startbutton.nearest:
                self.startbutton.update(nearest=True)
                self.startbutton.nearest = True

    def on_mouse_release(self, manager, x, y, buttons, modifiers):
        """Handle mouse release"""
        self.backbutton.on_mouse_release(x, y, buttons, modifiers)
        self.startbutton.on_mouse_release(x, y, buttons, modifiers)
        
    def name_update(self, val):
        """Check if name is valid"""
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
        self.nameinput.value = val
        

    def seed_update(self, val):
        
        if val == "":
            val = time.time()
        try:
            val = int(val)
        except:
            seed = 0
            for m, i in enumerate(val):
                seed += ord(i)*(m+1)
            val = seed

        
        self.seedinput.value = str(val)
        print(self.window.WORLD_PROPERTIES["seed"])

    def size_update(self, val):
        try:
            val = int(val)
        except:
            val = 10
        self.sizeinput.value = str(val)
        

    def back(self):
        self.manager.set_scene("menu")
    def next(self):
        """set the World properties and go to the next scene"""
        self.window.WORLD_PROPERTIES["name"] = self.nameinput.value
        self.window.WORLD_PROPERTIES["path"] = "saves/"+self.nameinput.value
        self.window.WORLD_PROPERTIES["seed"] = int(self.seedinput.value)
        self.window.WORLD_PROPERTIES["size"] = int(self.sizeinput.value)
        self.manager.set_scene("gen")
