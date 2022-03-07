from opensimplex import OpenSimplex
import numpy as np
import time

class Vertex(object):
	def __init__(self,x,y,z,humidity,temperature,erosion,fantasyness,evilness):
		self.x,self.y,self.z = x,y,z

		pass

def generateChunk(chunkName,SIZE=100,seed=13465,displacement=(0,0)):
	# Load perlin noise and set seed
	np.random.seed(int(seed))
	noise = OpenSimplex(seed)
	verts = {}
	tris = []
	normals = {}
	SIZE+=1
	Wavefront = 'mtllib blenderfile.mtl\no test\n'
	Wftris = ''
	Wfnormals = ''
	for x in range(0,SIZE):
		for y in range(0,SIZE):
			verts[SIZE*x+y] = (x+displacement[0],y+displacement[1],generateNoise(x+displacement[0],y+displacement[1],SIZE,noise))
			Wavefront += f'v {float(verts[SIZE*x+y][0])} {float(verts[SIZE*x+y][1])} {float(verts[SIZE*x+y][2])}\n'
			if x > 0 and y > 0:
				tris += [[SIZE*(x-1)+(y-1),SIZE*(x-1)+y,SIZE*x+y,'']]
			if x < SIZE-1 and y < SIZE-1:
				tris += [[SIZE*x+y, SIZE*(x+1)+(y+1), SIZE*(x+1)+y,'']]

	for i,tri in enumerate(tris):
		p1 = np.array(verts[tri[0]])
		p2 = np.array(verts[tri[1]])
		p3 = np.array(verts[tri[2]])
		tris[i][3] = i
		normals[i] = np.cross(p2-p1, p3-p1)
		Wfnormals += f'vn {normals[i][0]} {normals[i][1]} {normals[i][2]}\n'
		Wftris += f'f {tri[0]+1}//{tri[3]+1} {tri[1]+1}//{tri[3]+1} {tri[2]+1}//{tri[3]+1}\n'


	Wfnormals += 'usemtl Material\ns off\n'
	Wavefront += Wfnormals
	Wavefront += Wftris

	chunkName += '.obj'
	with open(chunkName,'w') as file:
		file.write(Wavefront)
		file.close()
	return True


def generateNoise(x,y,SIZE,noise,noise2=None,noise3=None,noise4=None,noise5=None):
	multiplier = 20
	scale = 0.15
	return noise.noise2d(x/SIZE*scale,y/SIZE*scale)*multiplier + 0.5*noise.noise2d(2*x/SIZE*scale,2*y/SIZE*scale)*multiplier + 0.25*noise.noise2d(4*x/SIZE*scale,4*y/SIZE*scale)*multiplier + 0.125*noise.noise2d(8*x/SIZE*scale,8*y/SIZE*scale)*multiplier + 0.0625*noise.noise2d(16*x/SIZE*scale,16*y/SIZE*scale)*multiplier

if __name__ == "__main__":
	generateChunk('test')
	generateChunk('test2',displacement(100,0))
