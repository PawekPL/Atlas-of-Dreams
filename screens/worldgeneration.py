"=======IMPORTS=========="

import json
import os
import random
import re
import shutil
import threading
import multiprocessing

import cv2
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
        """Vertex object to store data

        Args:
            x (int): X coordinate of the vertex
            y (int): Y coordinate of the vertex
            z (int): Z coordinate of the vertex
            type (string): vertex type
            humidity (float, optional): humidity value. Defaults to None.
            temperature (float, optional): temperature value. Defaults to None.
            erosion (float, optional): erosion value. Defaults to None.
            fantasyness (float, optional): fantasyness value. Defaults to None.
            evilness (float, optional): evilness value. Defaults to None.
            assetID (string, optional): ID of the asset. Defaults to None.
        """
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
        """Chunk object to store all vertices and generate PNG and OBJ files

        Args:
            chunkX (int): X coordinate of the chunk
            chunkZ (int): Z coordinate of the chunk
            noise (noise): terrain noise function
            noise_hu (noise): humidity noise function
            noise_te (noise): temperature noise function
            noise_er (noise): erosion noise function
            noise_fa (noise): fantasyness noise function
            noise_ev (noise): evilness noise function
            world_name (string): name of the world
            seed (int): seed for the noise functions
        """
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
                #if it is the edge of a chunk, create an edge vertex
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
                # special cases for the corners
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
                if (x, z) not in self.waterVertices:
                    # Generate assets
                    biome = self.vertices[(x, z)].biome
                    assets = BIOME_LIST[biome]["assets"]
                    #if the biome is a forrest, generate trees
                    if BIOME_LIST[biome]["type"] == "forrest":
                        #TODO Improve tree generation
                        chosen_asset = random.choice(assets)
                        chance = 1 // chosen_asset["chance"]
                        if random.randint(0, chance) == 0:
                            self.assetVertices[(x, z)] = Vertex(
                                x+self.chunkXc,
                                self.vertices[x][z].y,
                                z+self.chunkZc,
                                "a",
                                assetID=chosen_asset["name"])

                    else: #otherwise, load the assets using the biome
                        chosen_asset = random.choice(assets)
                        chance = 1 // chosen_asset["chance"]
                        if random.randint(0, chance) == 0:
                            #add an asset vertex to the chunk
                            self.assetVertices[(x, z)] = Vertex(
                                x+self.chunkXc,
                                self.vertices[x][z].y,
                                z+self.chunkZc,
                                "a",
                                assetID=chosen_asset["name"])
        # use threading to generate the PNG and OBJ files                    
        obj = threading.Thread(target=self.genOBJ)
        obj.start()
        png = threading.Thread(target=self.genPNG)
        png.start()
        png.join()
        obj.join()
        


    def genVertex(self, x, z, vtype):
        """Generate vertex at x, z with type vtype

        Args:
            x (int): x coordinate
            z (int): z coordinate
            vtype (str): type of vertex

        Returns:
            Vertex: Vertex object
        """
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
        """Generate OBJ file for the chunk"""
        
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
        #iterate through the vertices
        for x in range(self.size):
            for z in range(self.size):
                #add the vertex to the wavefront file
                wavefront += f"v {self.vertices[x,z].x} {self.vertices[x,z].y} {self.vertices[x,z].z}\n"
                
                #get the faces and edge faces for the vertex
                if x > 0 and z > 0:
                    tris.append(((x, z), (x-1, z-1), (x-1, z)))
                else:
                    edgetris.append(((x, z), (x, z-1),  (x-1, z)))

                if x < self.size-1 and z < self.size-1:
                    tris.append(((x+1, z), (x, z),  (x+1, z+1)))
                else:
                    edgetris.append(((x+1, z), (x, z),  (x, z+1)))
        #get the number of vertices
        offsetV = wavefront.count("v ")
        #iterate through the edge vertices
        for v in self.edgeVertices:
            wavefront += f"v {self.edgeVertices[v].x} {self.edgeVertices[v].y} {self.edgeVertices[v].z}\n"

        #iterate through the faces
        for i, triangle in enumerate(tris):
            # calculate the normal of the triangle
            p1 = np.array(
                [triangle[0][0], self.vertices[triangle[0]].y, triangle[0][1]])
            p2 = np.array(
                [triangle[1][0], self.vertices[triangle[1]].y, triangle[1][1]])
            p3 = np.array(
                [triangle[2][0], self.vertices[triangle[2]].y, triangle[2][1]])

            normals[i] = np.cross(p2-p1, p3-p1)
            # add the normal to the wavefront file
            wavefront_normals += f"vn {round(normals[i][0],4)} {round(normals[i][1],4)} {round(normals[i][2],4)}\n"
            # add the face to the wavefront file
            wavefront_tris += f"f {triangle[0][0]*self.size+triangle[0][1]+1}//{i+1} \
{triangle[1][0]*self.size+triangle[1][1]+1}//{i+1} \
{triangle[2][0]*self.size+triangle[2][1]+1}//{i+1}\n"
        #get the number of vertex normals
        offsetVN = wavefront_normals.count("vn ")
        #iterate through the edge faces
        for i, triangle in enumerate(edgetris):
            # calculate the normal of the edge triangle
            try:
                p1 = np.array(
                    [triangle[0][0], self.edgeVertices[triangle[0]].y, triangle[0][1]])
            except:
                p1 = np.array(
                    [triangle[0][0], self.vertices[triangle[0]].y, triangle[0][1]])
            try:
                p2 = np.array(
                    [triangle[1][0], self.edgeVertices[triangle[1]].y, triangle[1][1]])
            except:
                p2 = np.array(
                    [triangle[1][0], self.vertices[triangle[1]].y, triangle[1][1]])
            try:
                p3 = np.array(
                    [triangle[2][0], self.edgeVertices[triangle[2]].y, triangle[2][1]])
            except:
                p3 = np.array(
                    [triangle[2][0], self.vertices[triangle[2]].y, triangle[2][1]])
            
            edgeNormals[i] = np.cross(p2-p1, p3-p1)
            # add the normal to the wavefront file
            wavefront_normals += f"vn {round(edgeNormals[i][0],4)} {round(edgeNormals[i][1],4)} {round(edgeNormals[i][2],4)}\n"
            # add the face to the wavefront file
            try:
                r1 = list(self.edgeVertices).index(triangle[0])+offsetV+1
            except ValueError:
                r1 = int(p1[0]*self.size+p1[2]+1)
            try:
                r2 = list(self.edgeVertices).index(triangle[1])+offsetV+1
            except ValueError:
                r2 = int(p2[0]*self.size+p2[2]+1)

            try:
                r3 = list(self.edgeVertices).index(triangle[2])+offsetV+1
            except ValueError:
                r3 = int(p3[0]*self.size+p3[2]+1)

            wavefront_tris += f"f {r1}//{i+1+offsetVN} {r2}//{i+1+offsetVN} {r3}//{i+1+offsetVN}\n"
        #join all parts of the wavefront file
        wavefront += wavefront_normals
        wavefront += "usemtl None\n"
        wavefront += wavefront_tris
        #write the wavefront file to a file
        with open(f"saves/{self.world_name}/{name}.obj", "w") as f:
            f.write(wavefront)
            
        #copy the mtl files to the saves folder
        shutil.copy(
            "biomes/biome-colour-map.mtl",
            f"saves/{self.world_name}/biome-colour-map.mtl")
        # shutil.copy(
        #    "biomes/water-colour-map.mtl",
        #    f"saves/{self.world_name}/water-colour-map.mtl")
        shutil.copy(
            "biomes/assets.mtl",
            f"saves/{self.world_name}/assets.mtl")

        #try to make a directory for the chunk's assets
        try:
            os.mkdir(f"saves/{self.world_name}/{name}")
        except Exception as e:
            pass
        #generate the chunk's assets
        for asset in self.assetVertices:
            objpath = ASSET_LIST[self.assetVertices[asset].assetID]["objpath"]
            loadObjAsset(
                objpath,
                self.assetVertices[asset].x,
                self.assetVertices[asset].y,
                self.assetVertices[asset].z,
                f"saves/{self.world_name}/{name}/{asset[0]}_{asset[1]}.obj")
            

    def genPNG(self):
        """Generate PNG files of the chunk"""
        
        
        # chunk name that will be used as a filename
        name = f"{self.chunkX}_{self.chunkZ}"
        #image arrays
        chunk_img = np.full(
            ((self.size+2), (self.size+2), 3), 1, dtype=np.uint8)
        asset_img = np.zeros(
            ((self.size+2)*10, (self.size+2)*10, 4), dtype=np.uint8)
        height_img = np.zeros(
            ((self.size+2), (self.size+2), 4), dtype=np.uint8)
        #iterate through the arrays
        for x in range(self.size+2):
            for z in range(self.size+2):
                #If the vertex isn't on the edge of the chunk
                if (x != self.size+1 and z != self.size+1) and (x != 0 and z != 0):
                    #get the colour of the terrain vertex
                    color = np.array(
                        BIOME_LIST[self.vertices[x-1, z-1].biome]["color"])*255
                    #get the colour of the height vertex
                    b = int(self.vertices[x-1, z-1].y/60*1.45*200)
                #if the vertex is on the edge of the chunk
                else:
                    #get the colour of the terrain vertex
                    color = np.array(
                        BIOME_LIST[self.edgeVertices[(x-1, z-1)].biome]["color"])*255
                    #get the colour of the height vertex
                    b = int(self.edgeVertices[x-1, z-1].y/60*1.45*200)
                #set the colour of the terrain and height vertex
                hcolor = np.array([b, b, b, 150])
                height_img[x, z] = hcolor
                chunk_img[x, z] = color
        #resize the images
        height_img = cv2.resize(
            height_img, ((self.size+2)*10, (self.size+2)*10))
        chunk_img = cv2.resize(
            chunk_img, ((self.size+2)*10, (self.size+2)*10), interpolation=cv2.INTER_NEAREST)
        height_img[0:20, 0:] = np.zeros(4)
        height_img[0:, self.size*10:] = np.zeros(4)
        #iterate through the assets
        for asset in self.assetVertices:
            p1 = int((self.assetVertices[asset].x-self.chunkXc+1)*10-5)
            p2 = int((self.assetVertices[asset].x-self.chunkXc+1)*10+5)
            p3 = int((self.assetVertices[asset].z-self.chunkZc+1)*10-5)
            p4 = int((self.assetVertices[asset].z-self.chunkZc+1)*10+5)
            #get the image of the asset
            a = ASSET_PNGS[self.assetVertices[asset].assetID]
            #write the asset to the asset image
            asset_img[p1:p2, p3:p4] = np.where(
                asset_img[p1:p2, p3:p4] < a, a, a)
        #save the images
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

        self.name = name
        #try to delete a world with the same name
        try:
            shutil.rmtree(f"saves/{self.name}")
        except Exception as e:
            print(e)
        #create the world folder
        try:
            os.mkdir(f"saves/{self.name}")
        except Exception as e:
            pass
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
        self.chunks[(x, z)] = Chunk(
            x,
            z,
            self.noise,
            self.noise_hu,
            self.noise_te,
            self.noise_er,
            self.noise_fa,
            self.noise_ev,
            self.name,
            self.seed)


def loadObjAsset(path, x, y, z, filename):
    """Loads an asset from a .obj file.

    Args:
            path (str): The path to the .obj file
            x (int): The x coordinate of the asset
            y (int): The y coordinate of the asset
            z (int): The z coordinate of the asset
            filename (str): The name of the asset file

    Returns:
            str: The .obj file as a string
    """
    with open(path, "r") as f:
        lines = f.read()

        vertices = [i for i in re.finditer(
            r"v -?[0-9]+\.[0-9]+ -?[0-9]+\.[0-9]+ -?[0-9]+\.[0-9]+", lines, re.MULTILINE)]
        start = lines[0:vertices[0].start()]
        end = lines[vertices[-1].end():]
        newVert = ""

        for vert in vertices:
            vertex = vert.group()
            value = vertex.split(" ")
            value[1] = str(float(value[1]) + x)
            value[2] = str(float(value[2]) + y)
            value[3] = str(float(value[3]) + z)
            newVert += " ".join(value)+"\n"
        out = start + newVert + end

        with open(filename, "w") as f:
            f.write(out)


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
        # super().on_draw(manager)
        manager.window.clear()
        pyglet.gl.glClearColor(150/255, 150/255, 150/255, 1)
        # self.batch.draw()
        self.labelbatch.draw()

    def on_resize(self, manager, w, h):
        self.startlabel.x = manager.window.width//2
        self.startlabel.y = manager.window.height//2
        self.startlabel.font_size = manager.window.height//9
        # self.loading.update(w//4,3*h//8,w//2,h//16)
        pass

    def on_step(self, app, dt):
        try:
            #update the label
            self.startlabel.text = f"Generating World: {round((1 - len(self.world.queue)/(self.world.size**2))*100)}%"
        
            if len(self.world.queue) == 0:
                self.world.threads[-1].join()  # wait for last thread to finish
                self.world.threads[-2].join()
                self.world.threads[-3].join()
                #undeclare the world to save memory
                del self.world
                #change the scene to the 2D view
                app.set_scene("2Dview")
        except Exception as e:
            print(e)

    def on_load(self):
        #get the world properties
        name = self.window.WORLD_PROPERTIES["name"]
        size = self.window.WORLD_PROPERTIES["size"]
        seed = self.window.WORLD_PROPERTIES["seed"]
        #create the world
        self.world = World(name,size,seed)
        print(self.world)
