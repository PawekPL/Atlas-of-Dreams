"=======IMPORTS=========="

import json
import random
import re
import threading
import time

import noise  # pip install https://github.com/caseman/noise/archive/refs/heads/master.zip
import numpy as np
import pyglet
import scipy.spatial as sp
from libs.screen_manager import Scene
from libs.widgets import LoadingBar, updateLabel
from pyglet.gl import *
from pyglet.gui import *

"========================"

BIOME_LIST = json.load(open("biomes/biomes.json", "r"))  # List of biomes
BIOME_ARRAY = np.zeros((len(BIOME_LIST), 6))  # Array of biome attributes
for i in range(len(BIOME_LIST)):
    BIOME_ARRAY[i][0] = BIOME_LIST[i]["height"]
    BIOME_ARRAY[i][1] = BIOME_LIST[i]["temperature"]
    BIOME_ARRAY[i][2] = BIOME_LIST[i]["humidity"]
    BIOME_ARRAY[i][3] = BIOME_LIST[i]["erosion"]
    BIOME_ARRAY[i][4] = BIOME_LIST[i]["fantasyness"]
    BIOME_ARRAY[i][5] = BIOME_LIST[i]["evilness"]

BIOME_TREE = sp.cKDTree(BIOME_ARRAY)  # Tree of biome attributes


class Vertex(object):
    def __init__(self,
                 x, y, z,
                 type,
                 humidity=None,
                 temperature=None,
                 erosion=None,
                 fantasyness=None,
                 evilness=None,
                 assetID=None):
        self.x = x
        self.y = y
        self.z = z
        self._type = type  # There are 4 vertex types

        if self._type == "t":  # Terrain vertex
            self.humidity = humidity
            self.temperature = temperature
            self.erosion = erosion
            self.fantasyness = fantasyness
            self.evilness = evilness
            self.biome = self._getBiome()
            self.y = self._calculateHeight()
        elif self._type == "w":  # Water vertex
            pass
        elif self._type == "a":  # Asset vertex
            self.assetID = assetID
        elif self._type == "e":  # Edge vertex
            self.erosion = erosion
            self.y = self._calculateHeight()

    def _getBiome(self):
        """Get the biome of the vertex using the properties.

                Returns:
                        string: biomeID
                """
        return BIOME_TREE.query([self.y,
                                self.humidity,
                                self.temperature,
                                self.erosion,
                                self.fantasyness,
                                self.evilness])[1]

    def _calculateHeight(self):
        """ Calculate the actual height the vertex is placed at.
        60 will be the default height of the terrain."""
        return (1 + self.y + self.erosion/10) * 60


class Chunk(object):
    def __init__(self, chunkX, chunkZ, noise, noise_hu, noise_te, noise_er, noise_fa, noise_ev):
        self.size = 100
        self.scale = 2
        # create a numpy array with size of self.size
        self.vertices = np.empty((self.size, self.size), dtype=np.object)
        self.edgeVertices = {}
        self.assetVertices = {}
        self.waterVertices = {}
        chunkXc = chunkX * self.size * self.scale
        chunkZc = chunkZ * self.size * self.scale
        for x in range(self.size):
            for z in range(self.size):
                _x = (x*self.scale+chunkXc)/self.size
                _z = (z*self.scale+chunkZc)/self.size
                self.vertices[x][z] = Vertex(
                    _x,
                    noise(_x, _z),
                    _z,
                    "t",
                    humidity=noise_hu(_x, _z),
                    temperature=noise_te(_x*2, _z*2),
                    erosion=noise_er((_x+100/self.size)*10,
                                     (_z+100/self.size)*10),
                    fantasyness=noise_fa((_x+100)*4, (_z+100)*4),
                    evilness=noise_ev(_x, _x+_z, _z))

                if x == 0:
                    self.edgeVertices[(x-1, z)] = Vertex(
                        (x-1)*self.scale+chunkXc,
                        noise(
                            (x-1)*self.scale+chunkXc,
                            z*self.scale+chunkZc),
                        z*self.scale+chunkZc,
                        "e",
                        erosion=noise_er(
                            (((x-1)*self.scale+chunkXc)+100/self.size)*10, (_z+100/self.size)*10)
                    )
                elif x == self.size-1:
                    self.edgeVertices[(x+1, z)] = Vertex(
                        (x+1)*self.scale+chunkXc,
                        noise(
                            (x+1)*self.scale+chunkXc,
                            z*self.scale+chunkZc),
                        z*self.scale+chunkZc,
                        "e",
                        erosion=noise_er(
                            (((x+1)*self.scale+chunkXc)+100/self.size)*10, (_z+100/self.size)*10)
                    )
                if z == 0:
                    self.edgeVertices[(x, z-1)] = Vertex(
                        x*self.scale+chunkXc,
                        noise(
                            x*self.scale+chunkXc,
                            (z-1)*self.scale+chunkZc),
                        (z-1)*self.scale+chunkZc,
                        "e",
                        erosion=noise_er(
                            (_x+100/self.size)*10, (((z-1)*self.scale+chunkZc)+100/self.size)*10)
                    )
                elif z == self.size-1:
                    self.edgeVertices[(x, z+1)] = Vertex(
                        x*self.scale+chunkXc,
                        noise(
                            x*self.scale+chunkXc,
                            (z+1)*self.scale+chunkZc),
                        (z+1)*self.scale+chunkZc,
                        "e",
                        erosion=noise_er(
                            (_x+100/self.size)*10, (((z+1)*self.scale+chunkZc)+100/self.size)*10)
                    )
                # TODO: Add water vertices

                # check if water vertex exists above the terrain vertex
                try:
                    if self.waterVertices[(x, z)]:
                        pass
                except KeyError:
                    # Generate assets
                    biome = self.vertices[(x, z)].biome
                    if BIOME_LIST[biome]["name"] == "forrest":
                        pass  # TODO: Add tree generation
                    else:
                        assets = BIOME_LIST[biome]["assets"]
                        chosen_asset = random.choice(assets)
                        chance = 1 // chosen_asset["chance"]
                        if random.randint(0, chance) == 0:
                            self.assetVertices[(x, z)] = Vertex(_x,
                                                                self.vertices[x][z].y,
                                                                _z,
                                                                "a",
                                                                assetID=chosen_asset["name"])

    def genOBJ(self):
        tris = []
        normals = {}
        waterTris = []
        waterNormals = {}

        wavefront_tris = ''
        wavefront_normals = ''

        # chunk name taht will be used as a filename
        name = f"({self.chunkX}_{self.chunkZ})"
        wavefront = f"mtllib biome-colour-map.mtl\no {name}\n"
        wavefrontWater = f"mtllib water-colour-map.mtl\no {name}\n"

        for x in range(self.size):
            for z in range(self.size):
                wavefront += f"v {self.vertices[x,z].x} \
                    {self.vertices[x,z].z} \
                        {self.vertices[x,z].y}\n"
                if x > 0 and z > 0:
                    tris.append(((x-1, z-1), (x-1, z), (x, z)))
                if x < self.size-1 and z < self.size-1:
                    tris.append(((x, z), (x+1, z), (x+1, z+1)))


class World(object):
    def __init__(self, name, size, seed):
        """The World object that will contain the chunks,
and will be used to generate the world.

        Args:
                name (str): The name of the world.
                size (int): The initial world size
                seed (int): The world seed
        """

        self.name = name
        self.chunks = {}  # Using dict to store chunks instead of an array to allow for easy chunk editing and deletion
        np.random.seed(seed)
        self.size = size
        # Splitting noises into different variables so that it's clear where each noise is used.
        self.noise = noise.snoise2
        self.noise_hu = noise.pnoise2
        self.noise_te = noise.pnoise2
        self.noise_er = noise.snoise2
        self.noise_fa = noise.pnoise2
        self.noise_ev = noise.pnoise3

        self.queue = []
        self.threads = []
        self.genWorld()

    def genWorld(self):
        """Generates the world."""
        for x in range(self.size):
            for z in range(self.size):
                self.queue.append((x, z))

        pyglet.clock.schedule(self.createThread)
        # pyglet.clock.tick()

    def createThread(self, _):
        """Creates a thread to generate chunks."""
        self.threads.append(threading.Thread(target=self.genChunk))
        self.threads[-1].start()

    def genChunk(self):
        """Generates a chunk at the given coordinates.

        Args:
                x (int): The x coordinate of the chunk
                z (int): The z coordinate of the chunk
        """
        x, z = self.queue[0]
        self.queue.pop(0)
        if len(self.queue) == 0:
            pyglet.clock.unschedule(self.createThread)

        print(x, z)
        self.chunks[(x, z)] = Chunk(x,
                                    z,
                                    self.noise,
                                    self.noise_hu,
                                    self.noise_te,
                                    self.noise_er,
                                    self.noise_fa,
                                    self.noise_ev)


class WorldGen(Scene):
    def __init__(self, window):
        super().__init__()
        self.window = window
        self.labelbatch = pyglet.graphics.Batch()
        self.batch = pyglet.graphics.Batch()

        self.startlabel = pyglet.text.Label(
            "Generating World: 0%",
            font_size=self.window.height//9,
            x=self.window.width//2,
            y=self.window.height//2,
            batch=self.labelbatch,
            color=(0, 0, 0, 255),
            anchor_x='center',
            anchor_y='center')

    def on_draw(self, manager):
        #super().on_draw(manager)
        manager.window.clear()
        pyglet.gl.glClearColor(150/255, 150/255, 150/255, 1)
        #self.batch.draw()
        self.labelbatch.draw()

    def on_activate(self, manager):
        self.world = World("asd", 10, 1)

    def on_resize(self, manager, w, h):
        self.startlabel.x = w//2
        self.startlabel.y = h//2
        self.startlabel.font_size = h//9
        # self.loading.update(w//4,3*h//8,w//2,h//16)
        pass

    def on_step(self, app, dt):
        self.startlabel.text = f"Generating World: {round((1 - len(self.world.queue)/(self.world.size**2))*100)}%" 