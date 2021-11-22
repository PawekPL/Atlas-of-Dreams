from panda3d.core import *
from direct.showbase.ShowBase import ShowBase

loadPrcFileData("", "load-file-type p3assimp")

class MyApp(ShowBase):

    def __init__(self):

        ShowBase.__init__(self)

        model = self.loader.load_model("test.obj", )
        model.reparent_to(self.render)

app = MyApp()
app.run()
