from pyglet.gui import *


class OneTimeButton(PushButton):
    ''' Subclassing PushButton class from Pyglet in order to code in scaling '''
    def __init__(self,x, y, pressed, depressed, hover=None, batch=None, group=None):
        super().__init__(x, y, pressed, depressed, hover, batch, group)

    def update(self,x=None, y=None, width=None, height=None, scale=None, scale_x=None, scale_y=None):
        if x:
            self.x = x
        if y:
            self.y = y
        if x or y:
            self._update_position()
        if width:
            self._width = width
            pass
        if height:
            pass
        if scale:
            pass
        if scale_x:
            pass
        if scale_y:
            pass
        self._sprite.update(x=x, y=y, width=width, height=height, scale=scale, scale_x=scale_x, scale_y=scale_y)
        pass
