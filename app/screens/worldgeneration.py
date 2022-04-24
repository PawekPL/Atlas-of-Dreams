"=======IMPORTS=========="

import json
import random
import re
import threading
import os

import noise  # pip install https://github.com/caseman/noise/archive/refs/heads/master.zip
import numpy as np
import pyglet
import scipy.spatial as sp
import cv2
from libs.screen_manager import Scene
from libs.widgets import LoadingBar, updateLabel
from pyglet.gl import *
from pyglet.gui import *

"========================"

BIOME_LIST = json.load(open("biomes/biomes.json", "r"))  # List of biomes
BIOME_ARRAY = np.zeros((len(BIOME_LIST), 6))  # Array of biome attributes
ASSET_LIST = json.load(open("biomes/assets.json", "r"))  # List of assets

ASSET_PNGS = {}
for asset in ASSET_LIST:
    ASSET_PNGS[asset] = cv2.imread(
        ASSET_LIST[asset]["pngpath"], cv2.IMREAD_UNCHANGED)

for i, b in enumerate(BIOME_LIST):
    BIOME_ARRAY[i][0] = BIOME_LIST[b]["height"]
    BIOME_ARRAY[i][1] = BIOME_LIST[b]["temperature"]
    BIOME_ARRAY[i][2] = BIOME_LIST[b]["humidity"]
    BIOME_ARRAY[i][3] = BIOME_LIST[b]["erosion"]
    BIOME_ARRAY[i][4] = BIOME_LIST[b]["fantasyness"]
    BIOME_ARRAY[i][5] = BIOME_LIST[b]["evilness"]

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
            self.humidity = humidity
            self.temperature = temperature
            self.erosion = erosion
            self.fantasyness = fantasyness
            self.evilness = evilness
            self.biome = self._getBiome()
            self.y = self._calculateHeight()

    def _getBiome(self):
        """Get the biome of the vertex using the properties.

                Returns:
                        string: biomeID
                """
        return list(BIOME_LIST)[BIOME_TREE.query([self.y,
                                self.humidity,
                                self.temperature,
                                self.erosion,
                                self.fantasyness,
                                self.evilness])[1]]

    def _calculateHeight(self):
        """ Calculate the actual height the vertex is placed at.
        60 will be the default height of the terrain."""
        return ((1 + self.y/10) + self.erosion/100) * 60


class Chunk(object):
    def __init__(self, chunkX, chunkZ, noise, noise_hu, noise_te, noise_er, noise_fa, noise_ev, world_name, seed):
        self.world_name = world_name
        self.size = 50
        self.scale = 1
        self.chunkX = chunkX
        self.chunkZ = chunkZ
        self.seed = seed * 150
        # Set noises as class attributes
        self.noise = noise
        self.noise_hu = noise_hu
        self.noise_te = noise_te
        self.noise_er = noise_er
        self.noise_fa = noise_fa
        self.noise_ev = noise_ev
        # create a numpy array with size of self.size
        self.vertices = np.empty((self.size, self.size), dtype=np.object)
        self.edgeVertices = {}
        self.assetVertices = {}
        self.waterVertices = {}
        self.chunkXc = self.chunkX * self.size
        self.chunkZc = self.chunkZ * self.size
        for x in range(self.size):
            for z in range(self.size):
                _x = (x+self.chunkXc)/self.size
                _z = (z+self.chunkZc)/self.size
                self.vertices[x][z] = self.genVertex(_x, _z, "t")

                if x == 0:
                    self.edgeVertices[(x-1, z)] = self.genVertex(
                        (x+self.chunkXc-1)/self.size, _z, "e")

                elif x == self.size-1:
                    self.edgeVertices[(x+1, z)] = self.genVertex(
                        (x+self.chunkXc+1)/self.size, _z, "e")

                if z == 0:
                    self.edgeVertices[(x, z-1)] = self.genVertex(
                        _x, (z+self.chunkZc-1)/self.size, "e")

                elif z == self.size-1:
                    self.edgeVertices[(x, z+1)] = self.genVertex(
                        _x, (z+self.chunkZc+1)/self.size, "e")

                if x == 0 and z == 0:
                    self.edgeVertices[(x-1, z-1)] = self.genVertex(
                        (x+self.chunkXc-1)/self.size, (z+self.chunkZc-1)/self.size, "e")

                elif x == 0 and z == self.size-1:
                    self.edgeVertices[(x-1, z+1)] = self.genVertex(
                        (x+self.chunkXc-1)/self.size, (z+self.chunkZc+1)/self.size, "e")

                elif x == self.size-1 and z == 0:
                    self.edgeVertices[(x+1, z-1)] = self.genVertex(
                        (x+self.chunkXc+1)/self.size, (z+self.chunkZc-1)/self.size, "e")

                elif x == self.size-1 and z == self.size-1:
                    self.edgeVertices[(x+1, z+1)] = self.genVertex(
                        (x+self.chunkXc+1)/self.size, (z+self.chunkZc+1)/self.size, "e")

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
                            self.assetVertices[(x, z)] = Vertex(x+self.chunkXc,
                                                                self.vertices[x][z].y,
                                                                z+self.chunkZc,
                                                                "a",
                                                                assetID=chosen_asset["name"])

        # self.genOBJ()
        self.genPNG()

    def genVertex(self, x, z, vtype):
        return Vertex(
            x*self.size,
            self.noise(x/2, z/2, self.seed) +
            0.25*self.noise(x/8, z/8, self.seed) +
            0.125*self.noise(x/16, z/16, self.seed),
            z*self.size,
            vtype,
            humidity=self.noise_hu(x, z, self.seed),
            temperature=self.noise_te(x*2, z*2, self.seed),
            erosion=self.noise_er((x+100/self.size),
                                  (z+100/self.size), self.seed),
            fantasyness=self.noise_fa((x+100)*4, (z+100)*4, self.seed),
            evilness=self.noise_ev(x, x+z, self.seed))

    def genOBJ(self):
        tris = []
        normals = {}
        waterTris = []
        waterNormals = {}
        edgetris = []
        edgeNormals = {}

        wavefront_tris = ''
        wavefront_normals = ''

        # chunk name that will be used as a filename
        name = f"{self.chunkX}_{self.chunkZ}"
        wavefront = f"mtllib biome-colour-map.mtl\ng {name}\no {name}\n"
        wavefrontWater = f"mtllib water-colour-map.mtl\no {name}\n"

        for x in range(self.size):
            for z in range(self.size):
                wavefront += f"v {self.vertices[x,z].x} {self.vertices[x,z].z} {self.vertices[x,z].y}\n"
                if x > 0 and z > 0:
                    tris.append(((x-1, z-1), (x-1, z), (x, z)))
                else:
                    edgetris.append(((x-1, z), (x, z), (x, z-1)))

                if x < self.size-1 and z < self.size-1:
                    tris.append(((x, z), (x+1, z), (x+1, z+1)))
                else:
                    edgetris.append(((x+1, z), (x, z), (x, z+1)))

        offsetV = wavefront.count("v ")

        for v in self.edgeVertices:
            wavefront += f"v {self.edgeVertices[v].x} {self.edgeVertices[v].z} {self.edgeVertices[v].y}\n"

        for i, triangle in enumerate(tris):
            # calculate the normal of the triangle
            p1 = np.array(
                [triangle[0][0], self.vertices[triangle[0]].y, triangle[0][1]])
            p2 = np.array(
                [triangle[1][0], self.vertices[triangle[1]].y, triangle[1][1]])
            p3 = np.array(
                [triangle[2][0], self.vertices[triangle[2]].y, triangle[2][1]])

            normals[i] = np.cross(p2-p1, p3-p1)

            wavefront_normals += f"vn {round(normals[i][0],4)} {round(normals[i][1],4)} {round(normals[i][2],4)}\n"

            wavefront_tris += f"f {triangle[0][0]*self.size+triangle[0][1]+1}//{i+1} \
{triangle[1][0]*self.size+triangle[1][1]+1}//{i+1} \
{triangle[2][0]*self.size+triangle[2][1]+1}//{i+1}\n"

        offsetVN = wavefront_normals.count("vn ")

        for i, triangle in enumerate(edgetris):
            # calculate the normal of the edge triangle
            try:
                p1 = np.array(
                    [triangle[0][0], self.edgeVertices[triangle[0]].y, triangle[0][1]])
            except KeyError:
                p1 = np.array(
                    [triangle[0][0], self.vertices[triangle[0]].y, triangle[0][1]])
            p2 = np.array(
                [triangle[1][0], self.vertices[triangle[1]].y, triangle[1][1]])
            try:
                p3 = np.array(
                    [triangle[2][0], self.edgeVertices[triangle[2]].y, triangle[2][1]])
            except KeyError:
                p3 = np.array(
                    [triangle[2][0], self.vertices[triangle[2]].y, triangle[2][1]])

            edgeNormals[i] = np.cross(p2-p1, p3-p1)

            wavefront_normals += f"vn {round(edgeNormals[i][0],4)} {round(edgeNormals[i][1],4)} {round(edgeNormals[i][2],4)}\n"
            try:
                r1 = list(self.edgeVertices).index(triangle[0])+offsetV+1
            except ValueError:
                r1 = int(p1[0]*self.size+p1[2]+1)
            r2 = int(p2[0]*self.size+p2[2]+1)

            try:
                r3 = list(self.edgeVertices).index(triangle[2])+offsetV+1
            except ValueError:
                r3 = int(p3[0]*self.size+p3[2]+1)

            wavefront_tris += f"f {r1}//{i+1+offsetVN} {r2}//{i+1+offsetVN} {r3}//{i+1+offsetVN}\n"

        wavefront += wavefront_normals
        wavefront += "usemtl Default\ns off\n"
        wavefront += wavefront_tris

        for asset in self.assetVertices:
            offsetV = wavefront.count("v ")
            offsetVN = wavefront.count("vn ")
            objpath = ASSET_LIST[self.assetVertices[asset].assetID]["objpath"]
            wavefront += loadObjAsset(
                objpath, self.assetVertices[asset].x, self.assetVertices[asset].y, self.assetVertices[asset].z, offsetV, offsetVN)

        with open(f"saves/{self.world_name}/{name}.obj", "w") as f:
            f.write(wavefront)

    def genPNG(self):
        # chunk name that will be used as a filename
        name = f"{self.chunkX}_{self.chunkZ}"

        chunk_img = np.full(
            ((self.size+2), (self.size+2), 3), 1, dtype=np.uint8)
        asset_img = np.zeros(
            ((self.size+2)*10, (self.size+2)*10, 4), dtype=np.uint8)
        height_img = np.zeros(
            ((self.size+2), (self.size+2), 4), dtype=np.uint8)

        for x in range(self.size+2):
            for z in range(self.size+2):
                if (x != self.size+1 and z != self.size+1) and (x != 0 and z != 0):
                    color = np.array(
                        BIOME_LIST[self.vertices[x-1, z-1].biome]["color"])*255
                    b = int(self.vertices[x-1, z-1].y/60*1.45*200)

                else:
                    color = np.array(
                        BIOME_LIST[self.edgeVertices[(x-1, z-1)].biome]["color"])*255
                    b = int(self.edgeVertices[x-1, z-1].y/60*1.45*200)

                hcolor = np.array([b, b, b, 150])
                height_img[x, z] = hcolor
                chunk_img[x, z] = color

        height_img = cv2.resize(
            height_img, ((self.size+2)*10, (self.size+2)*10))
        chunk_img = cv2.resize(
            chunk_img, ((self.size+2)*10, (self.size+2)*10), interpolation=cv2.INTER_NEAREST)

        for asset in self.assetVertices:
            p1 = (self.assetVertices[asset].x-self.chunkXc+1)*10-5
            p2 = (self.assetVertices[asset].x-self.chunkXc+1)*10+5
            p3 = (self.assetVertices[asset].z-self.chunkZc+1)*10-5
            p4 = (self.assetVertices[asset].z-self.chunkZc+1)*10+5
            a = ASSET_PNGS[self.assetVertices[asset].assetID]
            asset_img[p1:p2, p3:p4] = np.where(
                asset_img[p1:p2, p3:p4] < a, a, a)

        cv2.imwrite(f"saves/{self.world_name}/{name}.png", chunk_img)
        cv2.imwrite(f"saves/{self.world_name}/{name}-assets.png", asset_img)
        cv2.imwrite(f"saves/{self.world_name}/{name}-height.png", height_img)


class World(object):
    def __init__(self, name, size, seed):
        """The World object that will contain the chunks,
and will be used to generate the world.

        Args:
                name (str): The name of the world.
                size (int): The initial world size
                seed (int): The world seed
        """

        self.name = name.replace("<", "")
        self.name = self.name.replace(">", "")
        self.name = self.name.replace("/", "")
        self.name = self.name.replace("\\", "")
        self.name = self.name.replace(":", "")
        self.name = self.name.replace("\"", "")
        self.name = self.name.replace("|", "")
        self.name = self.name.replace("?", "")
        self.name = self.name.replace("*", "")
        self.name = self.name.replace(".", "")
        try:
            os.mkdir(f"saves/{self.name}")
        except Exception as e:
            print(e)
        self.chunks = {}  # Using dict to store chunks instead of an array to allow for easy chunk editing and deletion
        np.random.seed(seed)
        random.seed(seed)
        self.seed = seed
        self.size = size
        # Splitting noises into different variables so that it's clear where each noise is used.
        self.noise = noise.snoise3
        self.noise_hu = noise.pnoise3
        self.noise_te = noise.pnoise3
        self.noise_er = noise.snoise3
        self.noise_fa = noise.pnoise3
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
                                    self.noise_ev,
                                    self.name,
                                    self.seed)


def loadObjAsset(path, x, y, z, offsetV, offsetVN, offsetVT=0):
    """Loads an asset from a .obj file.

    Args:
            path (str): The path to the .obj file
            x (int): The x coordinate of the asset
            y (int): The y coordinate of the asset
            z (int): The z coordinate of the asset
            offsetV (int): The offset of the vertices in the .obj file
            offsetVN (int): The offset of the normals in the .obj file

    Returns:
            str: The .obj file as a string
    """
    with open(path, "r") as f:
        lines = f.read()
        vertices = [i for i in re.finditer(
            r"v -?[0-9]+\.[0-9]+ -?[0-9]+\.[0-9]+ -?[0-9]+\.[0-9]+", lines, re.MULTILINE)]
        out = lines[0:vertices[0].start()]

        faces = [i for i in re.finditer(
            r"f(\ [0-9]{1,}\/([0-9])*\/([0-9]){1,}){3,4}(\n){0,1}", lines, re.MULTILINE)]
        mid = lines[vertices[-1].end()+1:faces[0].start()]

        for vert in vertices:
            vertex = vert.group()
            value = vertex.split(" ")
            value[1] = str(float(value[1]) + x)
            value[2] = str(float(value[2]) + z)
            value[3] = str(float(value[3]) + y)
            out += " ".join(value) + "\n"
        out += mid
        for f in faces:
            f = f.group()
            g = f.split(" ")
            for j, vertex in enumerate(g):
                if vertex == "f":
                    continue
                values = vertex.split("/")
                values[0] = str(int(values[0]) + offsetV)
                try:
                    values[1] = str(int(values[1]) + offsetVT)
                except:
                    pass
                values[2] = str(int(values[2]) + offsetVN)
                g[j] = "/".join(values)
            out += " ".join(g) + "\n"
        return out


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

        self.world = World("asdf", 10, 1)

    def on_draw(self, manager):
        # super().on_draw(manager)
        manager.window.clear()
        pyglet.gl.glClearColor(150/255, 150/255, 150/255, 1)
        # self.batch.draw()
        self.labelbatch.draw()

    def on_resize(self, manager, w, h):
        self.startlabel.x = w//2
        self.startlabel.y = h//2
        self.startlabel.font_size = h//9
        # self.loading.update(w//4,3*h//8,w//2,h//16)
        pass

    def on_step(self, app, dt):
        self.startlabel.text = f"Generating World: {round((1 - len(self.world.queue)/(self.world.size**2))*100)}%"
        if len(self.world.queue) == 0:
            self.world.threads[-1].join()  # wait for last thread to finish
            self.world.threads[-2].join()
            self.world.threads[-3].join()
            app.set_scene("menu")
