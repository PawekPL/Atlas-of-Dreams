
from pyglet_gui.manager import Manager
from pyglet_gui.buttons import Button
from pyglet_gui.scrollable import Scrollable
from pyglet_gui.containers import VerticalContainer

# Set up a Manager
Manager(
    # an horizontal layout with two vertical layouts, each one with a slider.
    Scrollable(height=100, width=200, content=VerticalContainer(content=[Button(str(x)) for x in range(10)])),
    window=window,
    batch=batch)

pyglet.app.run()
