import noise
import numpy as np
import time


class Vertex(object):
    def __init__(self, x, y, z, humidity, temperature, erosion, fantasyness, evilness):
        self.x, self.y, self.z = x, y, z

        pass


def generateChunk(chunkName, SIZE=100, seed=13465, displacement=(0, 0)):
    scale = 2
    # Load perlin noise and set seed
    np.random.seed(int(seed))
    verts = {}
    tris = []
    normals = {}
    Wavefront = 'mtllib blenderfile.mtl\no test\n'
    Wftris = ''
    Wfnormals = ''
    for x in range(0, SIZE):
        for y in range(0, SIZE):
            verts[SIZE*x+y] = (x*scale+displacement[0]*SIZE*scale, y*scale+displacement[1]*SIZE*scale,
                               generateNoise(x*scale+displacement[0]*SIZE*scale, y*scale+displacement[1]*SIZE*scale, SIZE))
            Wavefront += f'v {float(verts[SIZE*x+y][0])} {float(verts[SIZE*x+y][1])} {float(verts[SIZE*x+y][2])}\n'
            if x > 0 and y > 0:
                tris += [[SIZE*(x-1)+(y-1), SIZE*(x-1)+y, SIZE*x+y, '']]
            if x < SIZE-1 and y < SIZE-1:
                tris += [[SIZE*x+y, SIZE*(x+1)+(y+1), SIZE*(x+1)+y, '']]

    for i, tri in enumerate(tris):
        p1 = np.array(verts[tri[0]])
        p2 = np.array(verts[tri[1]])
        p3 = np.array(verts[tri[2]])
        tris[i][3] = i
        normals[i] = np.cross(p1-p2, p1-p3)*-1
        Wfnormals += f'vn {normals[i][0]} {normals[i][1]} {normals[i][2]}\n'
        Wftris += f'f {tri[0]+1}//{tri[3]+1} {tri[1]+1}//{tri[3]+1} {tri[2]+1}//{tri[3]+1}\n'

    Wfnormals += 'usemtl Material\ns off\n'
    Wavefront += Wfnormals
    Wavefront += Wftris

    chunkName += '.obj'
    with open(chunkName, 'w') as file:
        file.write(Wavefront)
        file.close()
    return True


def generateNoise(x, y, SIZE):
    multiplier = 10
    return noise.snoise2(x/SIZE, y/SIZE)*multiplier + 0.5*noise.snoise2(2*x/SIZE, 2*y/SIZE)*multiplier + 0.25*noise.snoise2(4*x/SIZE, 4*y/SIZE)*multiplier + 0.125*noise.snoise2(8*x/SIZE, 8*y/SIZE)*multiplier + 0.0625*noise.snoise2(16*x/SIZE, 16*y/SIZE)*multiplier


if __name__ == "__main__":
    generateChunk('hgfds')
    # generateChunk('test2',displacement(100,0))
