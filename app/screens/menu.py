from libs.screen_manager import Scene
import pyglet
import pyglet.gl
from pyglet_gui.manager import Manager
from pyglet_gui.buttons import Button, OneTimeButton, Checkbox, GroupButton
from pyglet_gui.containers import VerticalContainer
from pyglet_gui.theme import Theme

theme = Theme({"font": "Lucida Grande",
			   "font_size": 12,
			   "text_color": [255, 255, 255, 255],
			   "gui_color": [255, 0, 0, 255],
			   "button": {
				   "down": {
					   "image": {
						   "source": "button-down.png",
						   "frame": [6, 6, 3, 3],
						   "padding": [12, 12, 4, 2]
					   },
					   "text_color": [0, 0, 0, 255]
				   },
				   "up": {
					   "image": {
						   "source": "button.png",
						   "frame": [6, 6, 3, 3],
						   "padding": [12, 12, 4, 2]
					   }
				   }
			   }
			  }, resources_path='./assets/')

class Menu(Scene):
	def __init__(self):
		super().__init__()
		self.newButton = OneTimeButton(label="One time button")
		self.loadButton = OneTimeButton(label="One time button")
		pyglet.gl.glClearColor(0.5,0.4,0.6,1)
		self.batch = pyglet.graphics.Batch()
		Manager(VerticalContainer([
							self.newButton,
							self.loadButton]),
						window = None,
						batch = self.batch,
						theme = theme
						)


	def on_draw(self, manager):
		super().on_draw(manager)
		manager.window.clear()

		self.batch.draw()
