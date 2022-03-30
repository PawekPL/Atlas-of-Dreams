from libs.screen_manager import Scene
import pyglet
from pyglet.gl import *
from libs.widgets import OneTimeButton

import time

def output():
	print(time.time())

import types #Source: https://groups.google.com/g/pyglet-users/c/s8Icda9oPnY
def set_state(self):
	glEnable(self.texture.target)
	glBindTexture(self.texture.target, self.texture.id)
	glPushAttrib(GL_COLOR_BUFFER_BIT)
	glEnable(GL_BLEND)
	glTexParameteri(self.texture.target, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
	glBlendFunc(self.blend_src, self.blend_dest)

class Menu(Scene):
	def __init__(self,window):
		super().__init__()
		glEnable(GL_TEXTURE_2D)
		glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
		self.assetpos = [(515/1280,380/720),(515/1280,230/720),(515/1280,80/720),(540/1280,510/720)]
		self.assetsize = [(250/1280,120/720),(200/1280,200/720)]
		self.window = window

		self.pressed = pyglet.image.load("./assets/button-down.png")
		self.depressed = pyglet.image.load("./assets/button.png")
		self.logopng = pyglet.image.load("./assets/logo.png")

		self.batch = pyglet.graphics.Batch()
		self.frame = pyglet.gui.Frame(window, order=4)
		self.newbutton = OneTimeButton(self.assetpos[0][0]*self.window.width,
										self.assetpos[0][1]*self.window.height,
										self.pressed,
										self.depressed,
										batch=self.batch)

		self.newbutton.set_handler('on_release', output)
		self.frame.add_widget(self.newbutton)

		self.loadbutton = OneTimeButton(self.assetpos[1][0]*self.window.width,
										self.assetpos[1][1]*self.window.height,
										self.pressed,
										self.depressed,
										batch=self.batch)

		self.loadbutton.set_handler('on_release', output)
		self.frame.add_widget(self.loadbutton)

		self.settingsbutton = OneTimeButton(self.assetpos[2][0]*self.window.width,
											self.assetpos[2][1]*self.window.height,
											self.pressed,
											self.depressed,
											batch=self.batch)

		self.settingsbutton.set_handler('on_release', output)
		self.frame.add_widget(self.settingsbutton)

		self.logo = pyglet.sprite.Sprite(self.logopng,
										self.assetpos[3][0]*self.window.width,
										self.assetpos[3][1]*self.window.height,
										batch = self.batch)
		group = self.logo._group
		self.logo._group.set_state = types.MethodType(set_state, group)


		self.push_label = pyglet.text.Label("Push Button: False", x=300, y=300, batch=self.batch, color=(0, 0, 0, 255))


	def on_draw(self, manager):
		super().on_draw(manager)
		manager.window.clear()
		pyglet.gl.glClearColor(75/255, 0/255, 0/255, 1)
		self.batch.draw()

	def on_activate(self,manager):
		pass

	def on_resize(self,manager,w,h):
		self.newbutton.update(x=self.assetpos[0][0]*self.window.width,
								y=self.assetpos[0][1]*self.window.height,
								width=self.assetsize[0][0]*self.window.width,
								height=self.assetsize[0][1]*self.window.height,
								imgsize=(250,120),
								nearest=True)
		self.loadbutton.update(x=self.assetpos[1][0]*self.window.width,
								y=self.assetpos[1][1]*self.window.height,
								width=self.assetsize[0][0]*self.window.width,
								height=self.assetsize[0][1]*self.window.height,
								imgsize=(250,120),
								nearest=True)
		self.settingsbutton.update(x=self.assetpos[2][0]*self.window.width,
								y=self.assetpos[2][1]*self.window.height,
								width=self.assetsize[0][0]*self.window.width,
								height=self.assetsize[0][1]*self.window.height,
								imgsize=(250,120),
								nearest=True)

		self.logo.update(x=self.assetpos[3][0]*self.window.width,
								y=self.assetpos[3][1]*self.window.height,
								scale_x=self.assetsize[1][0]*self.window.width/200,
								scale_y=self.assetsize[1][1]*self.window.height/200)


	def on_mouse_press(self, manager, x, y, buttons, modifiers):

		self.newbutton.on_mouse_press(x, y, buttons, modifiers)
		self.loadbutton.on_mouse_press(x, y, buttons, modifiers)
		self.settingsbutton.on_mouse_press(x, y, buttons, modifiers)

		if self.newbutton.value:
			if not self.newbutton.nearest:
				self.newbutton.update(nearest=True)
				self.newbutton.nearest = True
		elif self.loadbutton.value:
			if not self.loadbutton.nearest:
				self.loadbutton.update(nearest=True)
				self.loadbutton.nearest = True
		elif self.settingsbutton.value:
			if not self.settingsbutton.nearest:
				self.settingsbutton.update(nearest=True)
				self.settingsbutton.nearest = True

	def on_mouse_release(self, manager, x, y, buttons, modifiers):
		self.newbutton.on_mouse_release(x, y, buttons, modifiers)
		self.loadbutton.on_mouse_release(x, y, buttons, modifiers)
		self.settingsbutton.on_mouse_release(x, y, buttons, modifiers)
