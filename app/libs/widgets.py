from pyglet.gui import *
from pyglet.gl import *

class OneTimeButton(PushButton):
    ''' Subclassing PushButton class from Pyglet in order to code in scaling and other transformations'''
    def __init__(self,x, y, pressed, depressed, hover=None, batch=None, group=None):
        super().__init__(x, y, pressed, depressed, hover, batch, group)
        self.nearest = False

    def update(self,x=None, y=None, width=None, height=None, nearest=None, imgsize=None):
        scale_x,scale_y = None,None
        if x:
            self._x = x
        if y:
            self._y = y
        if x or y:
            self._update_position()
        if width:
            self._width = int(width)
            scale_x = width/imgsize[0]

        if height:
            self._height = int(height)
            scale_y = height/imgsize[1]


        if nearest:  #if using nearest neighbor
            #Source: https://groups.google.com/g/pyglet-users/c/s8Icda9oPnY
            import types
            def set_state(self):
                glEnable(self.texture.target)
                glBindTexture(self.texture.target, self.texture.id)
                glPushAttrib(GL_COLOR_BUFFER_BIT)
                glEnable(GL_BLEND)
                glTexParameteri(self.texture.target, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
                glBlendFunc(self.blend_src, self.blend_dest)

            group = self._sprite._group
            self._sprite._group.set_state = types.MethodType(set_state, group)


        self._sprite.update(x=x, y=y, scale_x=scale_x, scale_y=scale_y)
