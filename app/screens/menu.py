from libs.screen_manager import Scene
import pyglet
import pyglet.gl

class Menu(Scene):
    def __init__(self):
        super().__init__()


    def on_draw(self, manager):
        super().on_draw(manager)
        manager.window.clear()
        pyglet.gl.glClearColor(0.5,0.4,0,1)
        
