
from perlin_noise import PerlinNoise as Perlin
import numpy as np
import time



SIZE = 100


noise = Perlin(octaves=1,seed=time.time())

verts = {}
tris = []
normals = {}

for x in range(0,SIZE):
    for y in range(0,SIZE):
        verts[SIZE*x+y] = (x,y,noise([x/SIZE,y/SIZE])*100)
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


Wavefront = 'o test\n'


for i in verts:
    Wavefront += f'v {float(verts[i][0])} {float(verts[i][1])} {float(verts[i][2])}\n'

for norm in normals:
    Wavefront += f'vn {normals[norm][0]} {normals[norm][1]} {normals[norm][2]}\n'

Wavefront += 'usemtl Default\ns off\n'

for tri in tris:
    Wavefront += f'f {tri[0]+1}//{tri[3]+1} {tri[1]+1}//{tri[3]+1} {tri[2]+1}//{tri[3]+1}\n'


with open('test.obj','w') as file:
    file.write(Wavefront)
    file.close()
