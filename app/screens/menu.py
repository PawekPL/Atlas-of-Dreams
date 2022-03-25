from libs.screen_manager import Scene
import pyglet
from pyglet.gl import *


import time

def output():
	print(time.time())

class Menu(Scene):
	def __init__(self,window):
		super().__init__()
		glEnable(GL_TEXTURE_2D)
		glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
		self.window = window

		self.pressed = pyglet.image.load("./assets/button-down.png")
		self.depressed = pyglet.image.load("./assets/button.png")

		self.batch = pyglet.graphics.Batch()
		self.frame = pyglet.gui.Frame(window, order=4)
		self.pushbutton = pyglet.gui.PushButton(100, 300, self.pressed, self.depressed, batch=self.batch)
		scale_x = self.window.width / 4 // self.pushbutton._sprite.width
		scale_y = self.window.height / 4 // self.pushbutton._sprite.height
		self.pushbutton._sprite.update(scale_x = scale_x,scale_y = scale_y)
		self.pushbutton._width = self.pushbutton._sprite.width
		self.pushbutton._height = self.pushbutton._sprite.height
		self.pushbutton.set_handler('on_release', output)
		self.frame.add_widget(self.pushbutton)
		self.push_label = pyglet.text.Label("Push Button: False", x=300, y=300, batch=self.batch, color=(0, 0, 0, 255))


	def on_draw(self, manager):
		super().on_draw(manager)
		manager.window.clear()
		pyglet.gl.glClearColor(0.5,0.4,0.6,1)
		self.batch.draw()

	def on_activate(self,manager):
		pass
