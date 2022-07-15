import json
import math
import os

import pyglet
from libs.screen_manager import Scene
from pyglet.gl import *
from pyglet.window import key

FOV = 70


class Cam:
    def __init__(self, pos=[25, 120, 25], rot=[-30, -135]):
        self.pos = pos
        self.rot = rot


class Chunk:
    def __init__(self, file, ):
        print(file)
        self.batch = pyglet.graphics.Batch()
        self.model = pyglet.model.load(file, batch=self.batch)
        self.assets = []

    def add_asset(self, asset):
        self.assets.append(
            pyglet.model.load(asset, batch=self.batch))

    def draw(self):
        self.batch.draw()


class View3D(Scene):
    def __init__(self, manager, window):
        super().__init__()
        self.window = window
        self.manager = manager
        # key handler
        self.keys = key.KeyStateHandler()
        self.window.push_handlers(self.keys)
        # load keybinds
        self.keybinds = json.load(open("config/settings.json"))["keybindings"]
        self.chunks = {}
        self.batch = pyglet.graphics.Batch()
        self.queue = []
        self.chunkqueue = {}

        self.camera = Cam()

    def on_load(self):
        self.world = self.window.WORLD_PROPERTIES["path"]
        return

    def chunkloader(self):
        """Read chunk from queue and create a model"""
        model = self.queue[0]
        if model not in self.chunks:
            self.chunks[model] = Chunk(self.world+model)
            for asset in self.chunkqueue[model]:
                self.chunks[model].add_asset(self.world+asset)

        self.queue.pop(0)

    def on_step(self, manager, dt):
        # if the queue isn't empty, load a chunk
        if self.queue != []:
            self.chunkloader()
        # move camera and check keybindings
        self.move_camera(dt)
        # iterate through 3x3 area of chunks
        try:
            for x in range(-1, 2):
                for y in range(-1, 2):
                    _x = int(self.camera.pos[0]//50+x)
                    _z = int(self.camera.pos[2]//50+y)
                    # if the chunk isn't loaded, add it to queue
                    if f"/{_x}_{_z}.obj" not in self.chunks and f"/{_x}_{_z}.obj" not in self.queue:
                        if os.path.exists(self.world+f"/{_x}_{_z}.obj"):
                            self.queue.append(
                                f"/{_x}_{_z}.obj")
                            # print(_x,_z)
                            self.chunkqueue[f"/{_x}_{_z}.obj"] = []
                            for asset in os.listdir(self.world+f"/{_x}_{_z}"):
                                self.chunkqueue[f"/{_x}_{_z}.obj"].append(
                                    f"/{_x}_{_z}/{asset}")
        except Exception as e:
            print(e)
        pass

    def move_camera(self, dt):
        # check keybinds
        if self.keys[self.keybinds["3d_pan_up"]]:
            self.camera.rot[0] += 30*dt
            print(self.camera.rot[0], self.camera.rot[1])
        if self.keys[self.keybinds["3d_pan_down"]]:
            self.camera.rot[0] -= 30*dt
            print(self.camera.rot[0], self.camera.rot[1])
        if self.keys[self.keybinds["3d_pan_left"]]:
            self.camera.rot[1] += 30*dt
            print(self.camera.rot[0], self.camera.rot[1])
        if self.keys[self.keybinds["3d_pan_right"]]:
            self.camera.rot[1] -= 30*dt
            print(self.camera.rot[0], self.camera.rot[1])
        # calculate movement
        dz, dx = math.sin(
            self.camera.rot[1]*math.pi/180)*dt, math.cos(self.camera.rot[1]*math.pi/180)*dt

        camera_speed = 10
        if self.keys[self.keybinds["3d_move_right"]]:
            self.camera.pos[0] += dx * camera_speed
            self.camera.pos[2] -= dz * camera_speed
            print(self.camera.pos[0], self.camera.pos[2])
        if self.keys[self.keybinds["3d_move_left"]]:
            self.camera.pos[0] -= dx * camera_speed
            self.camera.pos[2] += dz * camera_speed
            print(self.camera.pos[0], self.camera.pos[2])
        if self.keys[self.keybinds["3d_move_backward"]]:
            self.camera.pos[0] += dz * camera_speed
            self.camera.pos[2] += dx * camera_speed
            print(self.camera.pos[0], self.camera.pos[2])
        if self.keys[self.keybinds["3d_move_forward"]]:
            self.camera.pos[0] -= dz * camera_speed
            self.camera.pos[2] -= dx * camera_speed
            print(self.camera.pos[0], self.camera.pos[2])
        if self.keys[self.keybinds["3d_move_down"]]:
            self.camera.pos[1] -= camera_speed * dt
        if self.keys[self.keybinds["3d_move_up"]]:
            self.camera.pos[1] += camera_speed * dt


    def push(self):
        # Push the OpenGl matrix stack
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(FOV, self.window.width/self.window.height, 0.05, 1000)
        glPushMatrix()

        glRotatef(-self.camera.rot[0], 1, 0, 0)
        glRotatef(-self.camera.rot[1], 0, 1, 0)
        glTranslatef(-self.camera.pos[0],
                     -self.camera.pos[1],
                     -self.camera.pos[2],)

    def on_draw(self, manager):
        super().on_draw(manager)
        self.window.clear()
        glClearColor(0/255, 178/255, 255/255, 1)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_CULL_FACE)
        glCullFace(GL_BACK)

        self.push()

        for x in range(-1, 2):
            for y in range(-1, 2):
                _x = int(self.camera.pos[0]//50+x)
                _z = int(self.camera.pos[2]//50+y)

                if f"/{_x}_{_z}.obj" in self.chunks:
                    self.chunks[f"/{_x}_{_z}.obj"].draw()

        glMatrixMode(GL_PROJECTION)
        glPopMatrix()


    def on_activate(self, manager):
        pass

    def on_resize(self, manager, w, h):
        pass

    def on_mouse_press(self, manager, x, y, buttons, modifiers):
        pass

    def on_mouse_release(self, manager, x, y, buttons, modifiers):
        pass

    def on_key_release(self, manager, symbol, modifiers):
        if symbol == self.keybinds["main_menu"]:
            self.chunks = {}
            self.manager.set_scene("menu")
        if symbol == self.keybinds["viewmode_toggle"]:
            self.manager.set_scene("2Dview")
