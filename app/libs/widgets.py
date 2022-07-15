import types
from pyglet.gui import *
from pyglet.gl import *
from pyglet import shapes

# Procedure to update label properties
def updateLabel(label, x=None, y=None, font_size=None, color=None):
    if x:
        label.x = x
    if y:
        label.y = y
    if font_size:
        label.font_size = font_size
    if color:
        label.color = color
    pass


# Source: https://groups.google.com/g/pyglet-users/c/s8Icda9oPnY
def set_state(self):
    glEnable(self.texture.target)
    glBindTexture(self.texture.target, self.texture.id)
    glPushAttrib(GL_COLOR_BUFFER_BIT)
    glEnable(GL_BLEND)
    glTexParameteri(self.texture.target, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    glBlendFunc(self.blend_src, self.blend_dest)


class OneTimeButton(PushButton):
    ''' Subclassing PushButton class from Pyglet in order to code in scaling and other transformations'''

    def __init__(self, x, y, pressed, depressed, hover=None, batch=None, group=None):
        super().__init__(x, y, pressed, depressed, hover, batch, group)
        self.nearest = False
        self._z = 0

    def update(self, x=None, y=None, width=None, height=None, nearest=None, imgsize=None):
        scale_x, scale_y = None, None
        if x:
            self.position = x , self._y
        if y:
            self.position = self._x, y
        if width:
            self._width = int(width)
            scale_x = width/imgsize[0]

        if height:
            self._height = int(height)
            scale_y = height/imgsize[1]

        if nearest:  # if using nearest neighbor
            group = self._sprite._group
            self._sprite._group.set_state = types.MethodType(set_state, group)

        self._sprite.update(x=x, y=y, scale_x=scale_x, scale_y=scale_y)


class ToggleButton(OneTimeButton):
    """Instance of a toggle button sourced from pyglet.gui. The code was copied here,
    so that it inherits from OneTimeButton instead of PushButton.
    Triggers the event 'on_toggle' when the mouse is pressed or released.
    """

    def _get_release_image(self, x, y):
        return self._hover_img if self._check_hit(x, y) else self._depressed_img

    def on_mouse_press(self, x, y, buttons, modifiers):
        if not self.enabled or not self._check_hit(x, y):
            return
        self._pressed = not self._pressed
        self._sprite.image = self._pressed_img if self._pressed else self._get_release_image(
            x, y)
        self.dispatch_event('on_toggle', self._pressed)

    def on_mouse_release(self, x, y, buttons, modifiers):
        if not self.enabled or self._pressed:
            return
        self._sprite.image = self._get_release_image(x, y)


ToggleButton.register_event_type('on_toggle')


class LoadingBar(WidgetBase):
    """Loading bar is an object that draws rectangles 
to show progress of a task."""

    def __init__(self, x, y, width, height,
                 bg_color=(240, 240, 240), fg_color=(0, 200, 0), frame_color=(100, 100, 100),
                 batch=pyglet.graphics.Batch(),
                 group=pyglet.graphics.Group()):
        """Args:
            x (int): x coordinate of the loading bar
            y (int): y coordinate of the loading bar
            width (int): width of the loading bar
            height (int): height of the loading bar
            bg_color (tuple, optional): background color. Defaults to (240, 240, 240).
            fg_color (tuple, optional): foreground color. Defaults to (0, 200, 0).
            frame_color (tuple, optional): color of the frame. Defaults to (100, 100, 100).
            batch (pyglet.graphics.Batch, optional): Batch. Defaults to pyglet.graphics.Batch().
            group (pyglet.graphics.Group, optional): Group. Defaults to pyglet.graphics.OrderedGroup(0).
        """
        super().__init__(x, y, width, height)
        self._bg_color = bg_color
        self._fg_color = fg_color
        self._frame_color = frame_color
        self._batch = batch
        self._group = group

        self.border = self.height//8
        self._max_width = width - self.border*2

        self._value = 0.0
        # background rectangle
        self._background = shapes.BorderedRectangle(
            self._x,
            self._y,
            self._width,
            self._height,
            self.border,
            self._bg_color,
            self._frame_color,
            self._batch,
            self._group
        )
        # foreground rectangle
        self._foreground = shapes.Rectangle(
            self._x+self.border,
            self._y+self.border,
            self._value*self._max_width,
            self._height-self.border*2,
            self._fg_color,
            self._batch,
            self._group
        )

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        """Set the value of the loading bar."""
        # check if value is a float
        assert type(value) is float, "This Widget's value must be \
            a float between 0.0 and 1.0"
        # check if value is between 0.0 and 1.0 inclusive, if it is not, use the existing value 
        self._value = value if 0.0 <= value <= 1.0 else self._value
        #calculate the width of the foreground rectangle
        self._foreground.width = self._value*self._max_width

    def update(self, x=None, y=None, width=None, height=None):
        """Update the loading bar.

        Args:
            x (int, optional): x coordinate. Defaults to None.
            y (int, optional): y coordinate. Defaults to None.
            width (int, optional): width of the loading bar. Defaults to None.
            height (int, optional): height of the loading bar. Defaults to None.
        """
        self._x = x if x else self._x
        self._y = y if y else self._y
        self._width = width if width else self._width
        self._height = height if height else self._height
        self._background.x = self._x
        self._background.y = self._y
        self._background.width = self._width
        self._background.height = self._height
        self._foreground.x = self._x+self.border
        self._foreground.y = self._y+self.border
        self._foreground.width = self._value*self._max_width
        self._foreground.height = self._height-self.border*2

    def draw(self):
        """Draw the loading bar."""
        self._background.draw()
        self._foreground.draw()
