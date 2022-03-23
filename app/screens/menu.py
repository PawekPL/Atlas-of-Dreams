from libs.screen_manager import Scene
import pyglet
import pyglet.gl


import time

def output():
	print(time.time())

class Menu(Scene):
	def __init__(self,window):
		super().__init__()
		self.pressed = pyglet.image.load("./assets/button-down.png")
		self.depressed = pyglet.image.load("./assets/button.png")
		self.batch = pyglet.graphics.Batch()
		self.frame = pyglet.gui.Frame(window, order=4)
		self.pushbutton = pyglet.gui.PushButton(100, 300, self.pressed, self.depressed, batch=self.batch)
		self.pushbutton.set_handler('on_release', output)
		self.frame.add_widget(self.pushbutton)
		self.push_label = pyglet.text.Label("Push Button: False", x=300, y=300, batch=self.batch, color=(0, 0, 0, 255))
		self.window = window

	def on_draw(self, manager):
		super().on_draw(manager)
		manager.window.clear()
		pyglet.gl.glClearColor(0.5,0.4,0.6,1)
		self.batch.draw()

	def on_activate(self,manager):
		pass
