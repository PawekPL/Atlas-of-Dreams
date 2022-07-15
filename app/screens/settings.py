
import json

import pyglet
from libs.screen_manager import Scene
from pyglet.gl import *
from pyglet.gui import *
from libs.widgets import OneTimeButton, ToggleButton, updateLabel
from pyglet.window import key

KEYS = {
    # Keys taken from pyglet.window.key
    # ASCII commands
    0xff08: "BACKSPACE",
    0xff09: "TAB",
    0xff0a: "LINEFEED",
    0xff0b: "CLEAR",
    0xff0d: "ENTER",
    0xff13: "PAUSE",
    0xff14: "SCROLLLOCK",
    0xff15: "SYSREQ",
    0xff1b: "ESCAPE",
    0xff20: "SPACE",
    # Cursor control and motion
    0xff50: "HOME",
    0xff51: "LEFT",
    0xff52: "UP",
    0xff53: "RIGHT",
    0xff54: "DOWN",
    0xff55: "PAGEUP",
    0xff56: "PAGEDOWN",
    0xff57: "END",
    0xff58: "BEGIN",
    # Misc functions
    0xffff: "DELETE",
    0xff60: "SELECT",
    0xff61: "PRINT",
    0xff62: "EXECUTE",
    0xff63: "INSERT",
    0xff65: "UNDO",
    0xff66: "REDO",
    0xff67: "MENU",
    0xff68: "FIND",
    0xff69: "CANCEL",
    0xff6a: "HELP",
    0xff6b: "BREAK",
    0xff7e: "MODESWITCH",
    0xff7e: "SCRIPTSWITCH",
    0xffd2: "FUNCTION",
    # Number pad
    0xff7f: "NUMLOCK",
    0xff80: "NUM_SPACE",
    0xff89: "NUM_TAB",
    0xff8d: "NUM_ENTER",
    0xff91: "NUM_F1",
    0xff92: "NUM_F2",
    0xff93: "NUM_F3",
    0xff94: "NUM_F4",
    0xff95: "NUM_HOME",
    0xff96: "NUM_LEFT",
    0xff97: "NUM_UP",
    0xff98: "NUM_RIGHT",
    0xff99: "NUM_DOWN",
    0xff9a: "NUM_PRIOR",
    0xff9a: "NUM_PAGE_UP",
    0xff9b: "NUM_NEXT",
    0xff9b: "NUM_PAGE_DOWN",
    0xff9c: "NUM_END",
    0xff9d: "NUM_BEGIN",
    0xff9e: "NUM_INSERT",
    0xff9f: "NUM_DELETE",
    0xffbd: "NUM_EQUAL",
    0xffaa: "NUM_MULTIPLY",
    0xffab: "NUM_ADD",
    0xffac: "NUM_SEPARATOR",
    0xffad: "NUM_SUBTRACT",
    0xffae: "NUM_DECIMAL",
    0xffaf: "NUM_DIVIDE",
    0xffb0: "NUM_0",
    0xffb1: "NUM_1",
    0xffb2: "NUM_2",
    0xffb3: "NUM_3",
    0xffb4: "NUM_4",
    0xffb5: "NUM_5",
    0xffb6: "NUM_6",
    0xffb7: "NUM_7",
    0xffb8: "NUM_8",
    0xffb9: "NUM_9",
    # Function keys
    0xffbe: "F1",
    0xffbf: "F2",
    0xffc0: "F3",
    0xffc1: "F4",
    0xffc2: "F5",
    0xffc3: "F6",
    0xffc4: "F7",
    0xffc5: "F8",
    0xffc6: "F9",
    0xffc7: "F10",
    0xffc8: "F11",
    0xffc9: "F12",
    0xffca: "F13",
    0xffcb: "F14",
    0xffcc: "F15",
    0xffcd: "F16",
    0xffce: "F17",
    0xffcf: "F18",
    0xffd0: "F19",
    0xffd1: "F20",
    # Modifiers
    0xffe1: "LSHIFT",
    0xffe2: "RSHIFT",
    0xffe3: "LCTRL",
    0xffe4: "RCTRL",
    0xffe5: "CAPSLOCK",
    0xffe7: "LMETA",
    0xffe8: "RMETA",
    0xffe9: "LALT",
    0xffea: "RALT",
    0xffeb: "LWINDOWS",
    0xffec: "RWINDOWS",
    0xffed: "LCOMMAND",
    0xffee: "RCOMMAND",
    0xffef: "LOPTION",
    0xfff0: "ROPTION",
    # Latin-1
    0x020: "SPACE",
    0x021: "EXCLAMATION",
    0x022: "DOUBLEQUOTE",
    0x023: "HASH",
    0x024: "DOLLAR",
    0x025: "PERCENT",
    0x026: "AMPERSAND",
    0x027: "APOSTROPHE",
    0x028: "PARENLEFT",
    0x029: "PARENRIGHT",
    0x02a: "ASTERISK",
    0x02b: "PLUS",
    0x02c: "COMMA",
    0x02d: "MINUS",
    0x02e: "PERIOD",
    0x02f: "SLASH",
    0x030: "0",
    0x031: "1",
    0x032: "2",
    0x033: "3",
    0x034: "4",
    0x035: "5",
    0x036: "6",
    0x037: "7",
    0x038: "8",
    0x039: "9",
    0x03a: "COLON",
    0x03b: "SEMICOLON",
    0x03c: "LESS",
    0x03d: "EQUAL",
    0x03e: "GREATER",
    0x03f: "QUESTION",
    0x040: "AT",
    0x05b: "BRACKETLEFT",
    0x05c: "BACKSLASH",
    0x05d: "BRACKETRIGHT",
    0x05e: "ASCIICIRCUM",
    0x05f: "UNDERSCORE",
    0x060: "GRAVE",
    0x060: "QUOTELEFT",
    0x061: "A",
    0x062: "B",
    0x063: "C",
    0x064: "D",
    0x065: "E",
    0x066: "F",
    0x067: "G",
    0x068: "H",
    0x069: "I",
    0x06a: "J",
    0x06b: "K",
    0x06c: "L",
    0x06d: "M",
    0x06e: "N",
    0x06f: "O",
    0x070: "P",
    0x071: "Q",
    0x072: "R",
    0x073: "S",
    0x074: "T",
    0x075: "U",
    0x076: "V",
    0x077: "W",
    0x078: "X",
    0x079: "Y",
    0x07a: "Z",
    0x07b: "BRACELEFT",
    0x07c: "BAR",
    0x07d: "BRACERIGHT",
    0x07e: "ASCIITILDE"
}


class Settings(Scene):
    def __init__(self, manager, window):

        super().__init__()
        self.manager = manager
        # asset positions and sizes
        self.assetpos = [(40/1280, 640/720), (990/1280, 640/720),
                         (515/1280, 80/720), (540/1280, 510/720)]
        self.assetsize = [(250/1280, 60/720), (200/1280, 200/720)]

        self.window = window
        # key handler
        self.keys = key.KeyStateHandler()
        self.window.push_handlers(self.keys)
        # columns and rows for key bindings
        self.cols = [50/1280, 240/1280, 465 /
                     1280, 655/1280, 880/1280, 1070/1280]
        self.rows = [480/720, 390/720, 300/720, 210/720, 120/720, 30/720]
        # load button images
        self.pressed = pyglet.image.load("./assets/button-down.png")
        self.depressed = pyglet.image.load("./assets/button.png")
        # declare batches
        self.batch = pyglet.graphics.Batch()
        self.labelbatch = pyglet.graphics.Batch()
        # load settings
        self.settings = json.load(open("./config/settings.json"))
        self.settingslist = list(self.settings)

        # Button to go back to the main menu
        self.backbutton = OneTimeButton(
            self.assetpos[0][0]*self.window.width,
            self.assetpos[0][1]*self.window.height,
            self.pressed,
            self.depressed,
            batch=self.batch)

        self.backbutton.set_handler('on_release', self.back)

        self.backlabel = pyglet.text.Label(
            "Back",
            font_size=self.backbutton.height//5,
            x=self.backbutton.x+self.backbutton.width//2,
            y=self.backbutton.y+self.backbutton.height//2,
            batch=self.labelbatch,
            color=(0, 0, 0, 255),
            anchor_x='center',
            anchor_y='center')
        # Button to toggle vsync
        self.vsyncbutton = ToggleButton(
            972/1280*self.window.width,
            630/720*self.window.height,
            self.pressed,
            self.depressed,
            batch=self.batch)

        self.vsynclabel = pyglet.text.Label(
            "VSync:",
            font_size=self.window.height//60,
            x=785/1280*self.window.width,
            y=650/720*self.window.height,
            batch=self.labelbatch,
            anchor_x='left',
            anchor_y='bottom')

        # Button to toggle fps display
        self.framesbutton = ToggleButton(
            972/1280*self.window.width,
            550/720*self.window.height,
            self.pressed,
            self.depressed,
            batch=self.batch)

        self.frameslabel = pyglet.text.Label(
            "Show FPS:",
            font_size=self.window.height//60,
            x=785/1280*self.window.width,
            y=570/720*self.window.height,
            batch=self.labelbatch,
            anchor_x='left',
            anchor_y='bottom')

        # Lists to hold key buttons and labels
        self.keybuttons = []
        self.keylabels = []
        self.showlabels = []
        # iterate through columns and rows to create key buttons and labels
        for i, c in enumerate(self.cols):
            for j, r in enumerate(self.rows):
                # if the index is odd
                if i % 2 == 1:
                    # Add a key button
                    self.keybuttons.append(
                        ToggleButton(
                            c*self.window.width,
                            r*self.window.height,
                            self.pressed,
                            self.depressed,
                            batch=self.batch))
                    # Add a key label
                    self.showlabels.append(
                        pyglet.text.Label(
                            KEYS[self.settings["keybindings"][
                                list(
                                    self.settings["keybindings"]
                                )[
                                    i//2 *
                                    len(self.rows) +
                                    j
                                ]]],
                            font_size=self.keybuttons[-1].height//5,
                            x=self.keybuttons[-1].x +
                            self.keybuttons[-1].width//2,
                            y=self.keybuttons[-1].y +
                            self.keybuttons[-1].height//2,
                            batch=self.labelbatch,
                            anchor_x='center',
                            anchor_y='center'))
                    # Add an attribute to the key button
                    self.keybuttons[-1].rc = (r, c)
                # If the index is even
                else:
                    # Add a key label
                    self.keylabels.append(
                        pyglet.text.Label(
                            list(self.settings["keybindings"])[
                                i//2*len(self.rows)+j],
                            font_size=self.window.height//60,
                            x=c*self.window.width,
                            y=r*self.window.height,
                            batch=self.labelbatch,
                            anchor_x='left',
                            anchor_y='bottom'))
                    self.keylabels[-1].rc = (r, c)
        # declare a variable for the current key button
        self.keybind = None

    def on_draw(self, manager):
        super().on_draw(manager)
        manager.window.clear()
        pyglet.gl.glClearColor(75/255, 0/255, 0/255, 1)
        self.batch.draw()
        self.labelbatch.draw()

    def on_activate(self, manager):
        pass

    def on_resize(self, manager, w, h):
        """Update the button and label positions when the window is resized"""
        self.backbutton.update(
            x=self.assetpos[0][0]*self.window.width,
            y=self.assetpos[0][1]*self.window.height,
            width=self.assetsize[0][0]*self.window.width,
            height=self.assetsize[0][1]*self.window.height,
            imgsize=(250, 120),
            nearest=True)

        for i, button in enumerate(self.keybuttons):
            button.update(
                x=button.rc[1]*self.window.width,
                y=button.rc[0]*self.window.height,
                width=160/1280*self.window.width,
                height=60/720*self.window.height,
                nearest=True,
                imgsize=(250, 120))
            updateLabel(self.showlabels[i],
                        font_size=button.height//5,
                        x=button.x + button.width//2,
                        y=button.y + button.height//2)

        for label in self.keylabels:
            updateLabel(
                label,
                font_size=self.window.height//60,
                x=label.rc[1]*self.window.width,
                y=label.rc[0]*self.window.height+10)

        self.vsyncbutton.update(
            x=972/1280*self.window.width,
            y=630/720*self.window.height,
            width=160/1280*self.window.width,
            height=60/720*self.window.height,
            nearest=True,
            imgsize=(250, 120))

        self.framesbutton.update(
            x=972/1280*self.window.width,
            y=550/720*self.window.height,
            width=160/1280*self.window.width,
            height=60/720*self.window.height,
            nearest=True,
            imgsize=(250, 120))

        updateLabel(
            self.vsynclabel,
            font_size=self.window.height//60,
            x=785/1280*self.window.width,
            y=650/720*self.window.height)

        updateLabel(
            self.frameslabel,
            font_size=self.window.height//60,
            x=785/1280*self.window.width,
            y=570/720*self.window.height)

        updateLabel(
            self.backlabel,
            font_size=self.backbutton.height//5,
            x=self.backbutton.x+self.backbutton.width//2,
            y=self.backbutton.y+self.backbutton.height//2)

    def on_load(self):
        # Set the button values to the current settings
        self.vsyncbutton.value = self.settings['vsync']
        self.framesbutton.value = self.settings['show_fps']
        pass

    def on_step(self, manager, dt):
        # if the active keybind is not None and a key is pressed
        if self.keybind is not None and len(self.keys) != 0:
            for k in self.keys:
                if self.keys[k] == True:
                    # set the keybind to the pressed key
                    self.settings["keybindings"][self.keybind] = k
                    print(k)
                    index = list(
                        self.settings["keybindings"]
                    ).index(
                        self.keybind)
                    self.keybuttons[index].value = False
                    self.showlabels[index].text = KEYS[k]
                    self.keybind = None
                    break
        # save the settings
        json.dump(self.settings, open("config/settings.json", "w"))
        pass

    def on_text_motion_select(self, app, motion):
        pass

    def on_mouse_press(self, manager, x, y, buttons, modifiers):
        """Check if the mouse is pressed on a button"""
        self.vsyncbutton.on_mouse_press(x, y, buttons, modifiers)
        self.framesbutton.on_mouse_press(x, y, buttons, modifiers)
        keybindCheck = False
        for i, button in enumerate(self.keybuttons):
            button.on_mouse_press(x, y, buttons, modifiers)
            # if button was pressed
            if button.value:
                # check if the keybind value is already in use
                if self.keybind != list(self.settings["keybindings"])[i] and self.keybind is not None:
                    # if it is set the button back to False
                    button.value = False
                else:
                    # Otherwise set the keybind value using the pressed button
                    keybindCheck = True
                    self.keybind = list(self.settings["keybindings"])[i]
                    print(self.keybind)
            #if button was toggled off5
            elif not keybindCheck:
                self.keybind = None

        self.backbutton.on_mouse_press(x, y, buttons, modifiers)

        if self.backbutton.value:
            if not self.backbutton.nearest:
                self.backbutton.update(nearest=True)
                self.backbutton.nearest = True
        # check the value of the vsync button
        # turn vsync on or off
        if self.vsyncbutton.value:
            manager.window.set_vsync(True)
            self.settings["vsync"] = True
        elif not self.vsyncbutton.value:
            manager.window.set_vsync(False)
            self.settings["vsync"] = False
        # check the value of the frames button
        # show or hide the fps
        if self.framesbutton.value:
            manager.show_fps = True
            self.settings["show_fps"] = True
        elif not self.framesbutton.value:
            manager.show_fps = False
            self.settings["show_fps"] = False

    def on_mouse_release(self, manager, x, y, buttons, modifiers):
        self.backbutton.on_mouse_release(x, y, buttons, modifiers)

    def back(self):
        self.manager.set_scene("menu")
