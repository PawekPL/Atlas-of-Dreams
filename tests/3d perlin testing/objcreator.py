
from perlin_noise import PerlinNoise as Perlin
import numpy as np
import time



def generateChunk(chunkName,SIZE=300,seed=time.time()):
    # Load perlin noise and set seed
    noise = Perlin(octaves=1,seed=seed)
    noise2 = Perlin(octaves=2,seed=seed)
    noise3 = Perlin(octaves=4,seed=seed)
    noise4 = Perlin(octaves=8,seed=seed)
    noise5 = Perlin(octaves=16,seed=seed)

    verts = {}
    tris = []
    normals = {}

    Wavefront = 'o test\n'
    Wftris = ''
    Wfnormals = ''
    for x in range(0,SIZE):
        for y in range(0,SIZE):
            verts[SIZE*x+y] = (x,y,generateNoise(x,y,SIZE,noise,noise2,noise3,noise4,noise5))
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


    Wfnormals += 'usemtl Default\ns off\n'
    Wavefront += Wfnormals
    Wavefront += Wftris

    chunkName += '.obj'
    with open(chunkName,'w') as file:
        file.write(Wavefront)
        file.close()
    return True


def generateNoise(x,y,SIZE,noise,noise2=None,noise3=None,noise4=None,noise5=None):
    multiplier = 10
    return noise([x/SIZE,y/SIZE])*multiplier + 1*noise2([x/SIZE,y/SIZE])*multiplier + 0.5*noise3([x/SIZE,y/SIZE])*multiplier + 0.125*noise4([x/SIZE,y/SIZE])*multiplier + 0.0625*noise5([x/SIZE,y/SIZE])*multiplier

if __name__ == "__main__":
    generateChunk('test')
