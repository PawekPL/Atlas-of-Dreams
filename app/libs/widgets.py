from pyglet.gui import *
from pyglet.gl import *

class OneTimeButton(PushButton):
    ''' Subclassing PushButton class from Pyglet in order to code in scaling and other transformations'''
    def __init__(self,x, y, pressed, depressed, hover=None, batch=None, group=None):
        super().__init__(x, y, pressed, depressed, hover, batch, group)

    def update(self,x=None, y=None, width=None, height=None, scale=None, scale_x=None, scale_y=None,nearest=None):
        _scale_x = None
        _scale_y = None
        if x:
            self._x = x
        if y:
            self._y = y
        if x or y:
            self._update_position()
        if width:
            self._width = width
            _scale_x = width / self._sprite.width
        if height:
            self._height = height
            _scale_y = height / self._sprite.height
        if scale:
            self._width *= scale
            self._height *= scale
        if scale_x:
            self._width *= scale
        if scale_y:
            self._height *= scale
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

        scale_x = _scale_x or scale_x
        scale_y = _scale_y or scale_y

        self._sprite.update(x=x, y=y, scale=scale, scale_x=scale_x, scale_y=scale_y)
        print(2)
