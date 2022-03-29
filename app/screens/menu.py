from libs.screen_manager import Scene
import pyglet
from pyglet.gl import *
from libs.widgets import OneTimeButton

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
		self.pushbutton = OneTimeButton(100, 300, self.pressed, self.depressed, batch=self.batch)
		'''
		width = self.window.width / 4
		height = self.window.height / 4

		self.pushbutton.update(width = width,height = height,nearest = True)
		'''
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

	def on_resize(self,manager,w,h):
		width = w / 4
		height = h / 4

		self.pushbutton.update(width = width,height = height,nearest = True)
		print(3)
	def on_mouse_press(self, manager, x, y, buttons, modifiers):
		self.pushbutton.on_mouse_press(x, y, buttons, modifiers)

	def on_mouse_release(self, manager, x, y, buttons, modifiers):
		self.pushbutton.on_mouse_release(x, y, buttons, modifiers)
