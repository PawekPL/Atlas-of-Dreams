import pyglet
from pyglet.gl import *
from pyglet.window import key

import math



class Model(pyglet.graphics.Batch):
	def __init__(self,file):
		super().__init__()
		self.model= pyglet.model.load(file, batch=self)
class Cam:
	def __init__(self, pos = [0,0,0],rot = [0,0]):
		self.pos = pos
		self.rot = rot


class Window(pyglet.window.Window):
	def push(self,pos,rot): glPushMatrix(); glRotatef(-rot[0],1,0,0); glRotatef(-rot[1],0,1,0); glTranslatef(-pos[0],-pos[1],-pos[2],)

	def __init__(self,*args,**kwargs):
		super().__init__(*args,**kwargs)
		self.set_minimum_size(600,400)
		self.keys = key.KeyStateHandler()
		self.push_handlers(self.keys)
		pyglet.clock.schedule(self.update)

		self.model = Model("test.obj")
		self.camera = Cam()

	def on_draw(self):
		self.clear()
		self.model.draw()
		self.push(self.camera.pos,self.camera.rot)


	def update(self,dt):
		self.hotkeys()
		self.move_camera(dt)
		#self.mesh.rotation.y += dt*5
		pass

	def on_mouse_enter(self,x,y):
		self.set_exclusive_mouse(True)
	def on_mouse_motion(self,x,y,dx,dy):
		self.camera.rot[1] -= dx *0.1
		self.camera.rot[0] += dy *0.1
	def hotkeys(self):
		if self.keys[key.ESCAPE]: self.close()
	def move_camera(self,dt):
		dz,dx = math.sin(self.camera.rot[1]*math.pi/180)*dt,math.cos(self.camera.rot[1]*math.pi/180)*dt

		camera_speed = 3
		if self.keys[key.D]: self.camera.pos[0]+=dx; self.camera.pos[2]-=dz;print(dx/dt,dz/dt)
		if self.keys[key.A]: self.camera.pos[0]-=dx; self.camera.pos[2]+=dz;print(dx/dt,dz/dt)
		if self.keys[key.S]: self.camera.pos[0]+=dz; self.camera.pos[2]+=dx;print(dx/dt,dz/dt)
		if self.keys[key.W]: self.camera.pos[0]-=dz; self.camera.pos[2]-=dx;print(dx/dt,dz/dt)
		if self.keys[key.LSHIFT]:
			self.camera.pos[1] -= camera_speed * dt
		if self.keys[key.SPACE]:
			self.camera.pos[1] += camera_speed * dt

w = Window(resizable=True)
pyglet.app.run()
