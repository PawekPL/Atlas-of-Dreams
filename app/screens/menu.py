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
		self.buttonpos = [(515/1280,380/720)]
		self.buttonsize = [(250/1280,120/720)]
		self.window = window

		self.pressed = pyglet.image.load("./assets/button-down.png")
		self.depressed = pyglet.image.load("./assets/button.png")

		self.batch = pyglet.graphics.Batch()
		self.frame = pyglet.gui.Frame(window, order=4)
		self.pushbutton = OneTimeButton(self.buttonpos[0][0]*self.window.width,
										self.buttonpos[0][1]*self.window.height,
										self.pressed,
										self.depressed,
										batch=self.batch)

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
		self.pushbutton.update(x=self.buttonpos[0][0]*self.window.width,
								y=self.buttonpos[0][1]*self.window.height,
								width=self.buttonsize[0][0]*self.window.width,
								height=self.buttonsize[0][1]*self.window.height,
								imgsize=(250,120),
								nearest=True)

	def on_mouse_press(self, manager, x, y, buttons, modifiers):
		self.pushbutton.on_mouse_press(x, y, buttons, modifiers)
		if self.pushbutton.value:
			if not self.pushbutton.nearest:
				self.pushbutton.update(nearest=True)
				self.pushbutton.nearest = True

	def on_mouse_release(self, manager, x, y, buttons, modifiers):
		self.pushbutton.on_mouse_release(x, y, buttons, modifiers)
