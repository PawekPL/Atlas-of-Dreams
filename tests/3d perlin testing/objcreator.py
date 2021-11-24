from perlin_numpy import generate_perlin_noise_2d
import numpy as np
import time



def generateChunk(chunkName,SIZE=200,seed=time.time()):
    # Load perlin noise and set seed
    np.random.seed(int(seed))
    noise = generateNoise(SIZE)
    verts = {}
    tris = []
    normals = {}

    Wavefront = 'o test\n'
    Wftris = ''
    Wfnormals = ''
    for x in range(0,SIZE):
        for y in range(0,SIZE):
            verts[SIZE*x+y] = (x,y,noise[x,y])
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


def generateNoise(SIZE):
    multiplier = 50
    scale = 5
    return generate_perlin_noise_2d((SIZE,SIZE),(scale,scale))*multiplier + generate_perlin_noise_2d((SIZE,SIZE),(scale//2,scale//2))

if __name__ == "__main__":
    generateChunk('test')
