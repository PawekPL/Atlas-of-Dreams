from libs.screen_manager import Scene
import pyglet
from pyglet.gl import *
from libs.widgets import OneTimeButton,updateLabel,ToggleButton

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

class NewProject(Scene):
	def __init__(self,window):
		super().__init__()
		glEnable(GL_TEXTURE_2D)
		glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
		self.assetpos = [(40/1280,640/720),(990/1280,640/720),(515/1280,80/720),(540/1280,510/720)]
		self.assetsize = [(250/1280,60/720),(200/1280,200/720)]
		self.window = window

		self.pressed = pyglet.image.load("./assets/button-down.png")
		self.depressed = pyglet.image.load("./assets/button.png")

		self.batch = pyglet.graphics.Batch()
		self.labelbatch = pyglet.graphics.Batch()
		self.frame = pyglet.gui.Frame(window, order=4)

		# Button to go back to the main menu
		self.backbutton = OneTimeButton(self.assetpos[0][0]*self.window.width,
										self.assetpos[0][1]*self.window.height,
										self.pressed,
										self.depressed,
										batch=self.batch)

		self.backbutton.set_handler('on_release', output)
		self.frame.add_widget(self.backbutton)

		self.backlabel = pyglet.text.Label("Back",
                                       font_size=self.backbutton.height//5,
                                       x=self.backbutton.x+self.backbutton.width//2,
                                       y=self.backbutton.y+self.backbutton.height//2,
                                       batch=self.labelbatch,
                                       color=(0,0,0,255),
									   anchor_x='center',
									   anchor_y='center')


		# Button to go to the next scene
		self.startbutton = OneTimeButton(self.assetpos[1][0]*self.window.width,
										self.assetpos[1][1]*self.window.height,
										self.pressed,
										self.depressed,
										batch=self.batch)

		self.startbutton.set_handler('on_release', output)
		self.frame.add_widget(self.startbutton)

		self.startlabel = pyglet.text.Label("Load Project",
                                       font_size=self.startbutton.height//5,
                                       x=self.startbutton.x+self.startbutton.width//2,
                                       y=self.startbutton.y+self.startbutton.height//2,
                                       batch=self.labelbatch,
                                       color=(0,0,0,255),
									   anchor_x='center',
									   anchor_y='center')




	def on_draw(self, manager):
		super().on_draw(manager)
		manager.window.clear()
		pyglet.gl.glClearColor(75/255, 0/255, 0/255, 1)
		self.batch.draw()
		self.labelbatch.draw()

	def on_activate(self,manager):
		pass

	def on_resize(self,manager,w,h):
		self.backbutton.update(x=self.assetpos[0][0]*self.window.width,
								y=self.assetpos[0][1]*self.window.height,
								width=self.assetsize[0][0]*self.window.width,
								height=self.assetsize[0][1]*self.window.height,
								imgsize=(250,120),
								nearest=True)
		self.startbutton.update(x=self.assetpos[1][0]*self.window.width,
								y=self.assetpos[1][1]*self.window.height,
								width=self.assetsize[0][0]*self.window.width,
								height=self.assetsize[0][1]*self.window.height,
								imgsize=(250,120),
								nearest=True)

		updateLabel(self.backlabel,
					font_size=self.backbutton.height//5,
					x=self.backbutton.x+self.backbutton.width//2,
					y=self.backbutton.y+self.backbutton.height//2)

		updateLabel(self.startlabel,
					font_size=self.startbutton.height//5,
					x=self.startbutton.x+self.startbutton.width//2,
					y=self.startbutton.y+self.startbutton.height//2)



	def on_mouse_press(self, manager, x, y, buttons, modifiers):

		self.backbutton.on_mouse_press(x, y, buttons, modifiers)
		self.startbutton.on_mouse_press(x, y, buttons, modifiers)

		if self.backbutton.value:
			if not self.backbutton.nearest:
				self.backbutton.update(nearest=True)
				self.backbutton.nearest = True

		elif self.startbutton.value:
			if not self.startbutton.nearest:
				self.startbutton.update(nearest=True)
				self.startbutton.nearest = True


	def on_mouse_release(self, manager, x, y, buttons, modifiers):
		self.backbutton.on_mouse_release(x, y, buttons, modifiers)
		self.startbutton.on_mouse_release(x, y, buttons, modifiers)
