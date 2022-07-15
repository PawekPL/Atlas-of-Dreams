import pyglet
from libs.screen_manager import Scene
from pyglet.window import key
from pyglet.gui import *
from libs.widgets import *
import os
import json



class View2D(Scene):
    def __init__(self,manager, window):
        super().__init__()
        self.window = window
        self.manager = manager
        #initiate key handler
        self.keys = key.KeyStateHandler()
        self.window.push_handlers(self.keys)
        #initialize batches
        self.terrain_batch = pyglet.graphics.Batch()
        self.heightmap_batch = pyglet.graphics.Batch()
        self.asset_batch = pyglet.graphics.Batch()
        self.gui_batch = pyglet.graphics.Batch()
        self.terrain_group = pyglet.graphics.Group()
        self.heightmap_group = pyglet.graphics.Group()
        self.asset_group = pyglet.graphics.Group()
        #define dictionaries to store chunks
        self.tchunks = {}
        self.hchunks = {}
        self.achunks = {}
        #define a cursor and a virtual cursor
        self.cursor = [50, 50]
        self.vcursor = [self.window.width//2, self.window.height//2]
        self.scale = 1

    def on_load(self):
        #get keybinds
        self.keybinds = json.load(open("config/settings.json"))["keybindings"]
        #self.window.WORLD_PROPERTIES["world_path"] = "saves/Project Name/"
        #get world properities
        self.properties = self.window.WORLD_PROPERTIES
        #check if the chunks are empty
        if self.tchunks == {} and self.hchunks == {} and self.achunks == {}:
            #for every file in the world directory
            for chunk in os.listdir(self.properties["path"]):
                #if the file is a PNG
                if ".png" in chunk:
                    #load the chunk
                    img = pyglet.image.load(self.properties["path"]+"/"+chunk)
                    y, x = chunk[:-4].split("_")
                    #if the chunk is an asset chunk
                    if "assets" in chunk:
                        #add the chunk to the asset dictionary
                        self.achunks[(x[:-7], y)] = pyglet.sprite.Sprite(
                            img,
                            x=int(x[:-7])*(img.width-20),
                            y=int(y)*-(img.height-20),
                            batch=self.asset_batch,
                            group=self.asset_group)
                        self.achunks[(x[:-7], y)]._group.set_state = types.MethodType(set_state, self.achunks[(x[:-7], y)]._group)
                    #if the chunk is a heightmap chunk
                    elif "height" in chunk:
                        #add the chunk to the heightmap dictionary
                        self.hchunks[(x[:-7], y)] = pyglet.sprite.Sprite(
                            img,
                            x=int(x[:-7])*(img.width-20),
                            y=int(y)*-(img.height-20),
                            batch=self.heightmap_batch,
                            group=self.heightmap_group)
                        self.hchunks[(x[:-7], y)]._group.set_state = types.MethodType(set_state, self.hchunks[(x[:-7], y)]._group)
                    #otherwise (if the chunk is a terrain chunk)
                    else:
                        #add the chunk to the terrain dictionary
                        self.tchunks[(x, y)] = pyglet.sprite.Sprite(
                            img,
                            x=int(x)*(img.width-20),
                            y=int(y)*-(img.height-20),
                            batch=self.terrain_batch,
                            group=self.terrain_group)
                        self.tchunks[(x, y)]._group.set_state = types.MethodType(set_state, self.tchunks[(x, y)]._group)
        

    def on_draw(self, app):
        #clear context
        self.window.clear()
        glClearColor(221/255, 200/255, 265/255, 1.0)

        #draw the batches
        super().on_draw(app)
        self.terrain_batch.draw()
        self.heightmap_batch.draw()
        self.asset_batch.draw()

    def on_step(self, app, dt):
        #Check if keybinds have been pressed
        if self.keys[self.keybinds["2d_move_left"]]:
            self.cursor[0] += 100*dt
        if self.keys[self.keybinds["2d_move_right"]]:
            self.cursor[0] -= 100*dt
        if self.keys[self.keybinds["2d_move_up"]]:
            self.cursor[1] -= 100*dt
        if self.keys[self.keybinds["2d_move_down"]]:
            self.cursor[1] += 100*dt
        if self.keys[self.keybinds["2d_zoom_in"]]:
            self.scale += 0.01
        if self.keys[self.keybinds["2d_zoom_out"]]:
            self.scale -= 0.01
        if self.scale < 0.1:
            self.scale = 0.1
        
        
        #update the virtual cursor
        self.vcursor = self.window.width/2, self.window.height/2
        #iterate through the chunks
        for chunk in self.tchunks:
            #set the terrain chunk's scale
            self.tchunks[chunk].scale = self.scale
            #set the terrain chunk's position
            self.tchunks[chunk].x = int(chunk[0])*(
                self.tchunks[chunk].width-20*self.scale) + self.cursor[0]*self.scale -(self.vcursor[0]-self.window.width//2)//2
            self.tchunks[chunk].y = int(chunk[1])*(
                -self.tchunks[chunk].height+20*self.scale) + self.cursor[1]*self.scale +(self.vcursor[1]-self.window.height//2)//2
            #set the heightmap chunk's scale
            self.hchunks[chunk].scale = self.scale
            #set the heightmap chunk's position
            self.hchunks[chunk].x = int(chunk[0])*(
                self.hchunks[chunk].width-20*self.scale) + self.cursor[0]*self.scale-(self.vcursor[0]-self.window.width//2)//2
            self.hchunks[chunk].y = int(chunk[1])*(
                -self.hchunks[chunk].height+20*self.scale) + self.cursor[1]*self.scale+(self.vcursor[1]-self.window.height//2)//2
            #set the asset chunk's scale
            self.achunks[chunk].scale = self.scale
            #set the asset chunk's position
            self.achunks[chunk].x = int(chunk[0])*(
                self.achunks[chunk].width-20*self.scale) + self.cursor[0]*self.scale-(self.vcursor[0]-self.window.width//2)//2
            self.achunks[chunk].y = int(chunk[1])*(
                -self.achunks[chunk].height+20*self.scale) + self.cursor[1]*self.scale+(self.vcursor[1]-self.window.height//2)/2

    def on_key_release(self,app,symbol,mod):
        if symbol == self.keybinds["main_menu"]:
            self.tchunks = {}
            self.hchunks = {}
            self.achunks = {}
            self.manager.set_scene("menu")
        if symbol == self.keybinds["viewmode_toggle"]:
            self.manager.set_scene("3Dview")
