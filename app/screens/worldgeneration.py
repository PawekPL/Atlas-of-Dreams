from libs.screen_manager import Scene
import pyglet
from pyglet.gl import *
from pyglet.gui import *
from libs.widgets import OneTimeButton,updateLabel,ToggleButton

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
		return (1 + y + erosion/10) * 60





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
