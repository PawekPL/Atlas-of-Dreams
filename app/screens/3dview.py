import pyglet


class NewProject(Scene):
    def __init__(self, window):
        super().__init__()

        self.window = window
        self.window.params = {"name": "New Project",
                              "seed": 0,
                              "gen_structures": True,
                              }

        self.batch = pyglet.graphics.Batch()
        self.labelbatch = pyglet.graphics.Batch()
        

    def on_draw(self, manager):
        super().on_draw(manager)
        manager.window.clear()
        pyglet.gl.glClearColor(75/255, 0/255, 0/255, 1)
        self.batch.draw()
        self.labelbatch.draw()

    def on_activate(self, manager):
        pass

    def on_resize(self, manager, w, h):
        pass

    def on_mouse_press(self, manager, x, y, buttons, modifiers):
        pass

    def on_mouse_release(self, manager, x, y, buttons, modifiers):
        pass
