from matplotlib import scale
from numpy import size
from libs.screen_manager import Scene
import pyglet
from pyglet.gl import *
from pyglet.gui import *
from libs.widgets import OneTimeButton,updateLabel,ToggleButton
import numpy as np
import scipy 
import time, re

class Vertex(object):
	def __init__(self,
			x,y,z,
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
		self._type = type #There are 4 vertex types

		if self._type == "t": #Terrain vertex
			self.humidity = humidity
			self.temperature = temperature
			self.erosion = erosion
			self.fantasyness = fantasyness
			self.evilness = evilness
			self.biome = self._getBiome()
			self.y = self._calculateHeight()
		elif self._type == "w": #Water vertex
			pass
		elif self._type == "a": #Asset vertex
			self.assetID = assetID
		elif self._type == "e": #Edge vertex
			self.y = self._calculateHeight()

	def _getBiome(self):
		return None
		# find the closest biome to the values and return its id
		return biomeTree.query([self.y,
						self.humidity,
						self.temperature,
						self.erosion,
						self.fantasyness,
						self.evilness])[1]
	def _calculateHeight(self):
		# Calculate the actual height the vertex is placed at.
		# 60 will be the default height
		return (1 + self.y + self.erosion/10) * 60

class Chunk(object):
	def __init__(self,noise,noise_hu,noise_te,noise_er,noise_fa,noise_ev,chunkX,chunkZ):
		self.size = 100
		self.scale = 2
		#create a numpy array with size of self.size
		self.vertices = np.zeros((self.size,self.size))
		self.edgeVertices = {}
		self.assetVertices = {}
		self.waterVertices = {}
		chunkXc = chunkX * self.size * self.scale
		chunkZc = chunkZ * self.size * self.scale
		for x in range(self.size):
			for z in range(self.size):
				_x = x*scale+chunkXc
				_z = z*scale+chunkZc
				self.vertices[x][z] = Vertex(
					_x,
					noise(_x,_z),
					_z,
					"t",
					humidity=noise_hu(_x,_z),
					temperature=noise_te(_x,_z),
					erosion=noise_er(_x,_z),
					fantasyness=noise_fa(_x,_z),
					evilness=noise_ev(_x,_z))
				if x == 0:
					self.edgeVertices[(x-1,z)] = Vertex(
		 								(x-1)*scale+chunkXc,
										noise(
											(x-1)*scale+chunkXc,
											z*scale+chunkZc),
										z*scale+chunkZc,
          								"e",
                  						erosion=noise_er(
											(x-1)*scale+chunkXc,
											z*scale+chunkZc)
                        )
				elif x == self.size-1:
					self.edgeVertices[(x+1,z)] = Vertex(
										(x+1)*scale+chunkXc,
										noise(
											(x+1)*scale+chunkXc,
											z*scale+chunkZc),
										z*scale+chunkZc,
		  								"e",
				  						erosion=noise_er(
											(x+1)*scale+chunkXc,
											z*scale+chunkZc)
						)
				if z == 0:
					self.edgeVertices[(x,z-1)] = Vertex(
										x*scale+chunkXc,
										noise(
											x*scale+chunkXc,
											(z-1)*scale+chunkZc),
										(z-1)*scale+chunkZc,
										"e",
										erosion=noise_er(
											x*scale+chunkXc,
											(z-1)*scale+chunkZc)
						)
				elif z == self.size-1:
					self.edgeVertices[(x,z+1)] = Vertex(
										x*scale+chunkXc,
										noise(
											x*scale+chunkXc,
											(z+1)*scale+chunkZc),
										(z+1)*scale+chunkZc,
										"e",
										erosion=noise_er(
											x*scale+chunkXc,
											(z+1)*scale+chunkZc)
						)
				#TODO: Add water vertices

				#check if water vertex exists above the terrain vertex
				try:
					if self.waterVertices[(x,z)]:
						pass
				except KeyError:
					#Generate assets
					biome = self.vertices[(x,z)].biome
					if biome == "forrest":
						#TODO: Add tree generation
					else:
						assets = BIOMELIST[biome]["Assets"]
						chosen_asset = random.choice(assets)
						chance = 1 // chosen_asset["Chance"]
						if random.randint(0,chance) == 0:
							self.assetVertices[(x,z)] = Vertex(_x,
                                          self.vertices[x][z].y,
                                          _z,
                                          "a",
                                          assetID = chosen_asset["Name"])
	def genOBJ(self):
		tris = []
		normals = {}
		waterTris = []
		waterNormals = {}

		wavefront_tris = ''
		wavefront_normals = ''

		name = f"({self.chunkX}_{self.chunkZ})" #chunk name taht will be used as a filename
		wavefront = f"mtllib biome-colour-map.mtl\no {name}\n"
		wavefrontWater = "mtllib water-colour-map.mtl\no {name}\n"

		for x in range(self.size):
			for z in range(self.size):
				wavefront += f"v {vertices[x,z].x} {vertices[x,z].z} {vertices[x,z].y}\n"
				if x > 0 and z > 0:
					tris.append(((x-1,z-1),(x-1,z),(x,z)))
				if x < self.size-1 and z < self.size-1:
					tris.append(((x,z),(x+1,z),(x+1,z+1)))
		

  
  


				
			
    

    

    


class WorldGen(Scene):
	def __init__(self,window):
		super().__init__()
		self.window = window
		self.labelbatch = pyglet.graphics.Batch()
		self.frame = pyglet.gui.Frame(window, order=4)

		self.startlabel = pyglet.text.Label(
			"Generating World",
			font_size=self.window.height//7,
			x=self.window.width//2,
			y=self.window.height//2,
			batch=self.labelbatch,
			color=(0,0,0,255),
			anchor_x='center',
			anchor_y='center')

		self.v = Vertex(0,0,0,"t",0,0,0,0,0,0)
		self.c = Chunk(0,0,0,0,0,0,0,0)


	def on_draw(self, manager):
		super().on_draw(manager)
		manager.window.clear()
		pyglet.gl.glClearColor(220/255, 220/255, 200/255, 1)
		self.labelbatch.draw()


	def on_activate(self,manager):
		pass

	def on_resize(self,manager,w,h):
		pass

	def on_mouse_press(self, manager, x, y, buttons, modifiers):
		self.frame.on_mouse_press(x,y,buttons,modifiers)


	def on_mouse_release(self, manager, x, y, buttons, modifiers):
		self.frame.on_mouse_release(x,y,buttons,modifiers)
