import timeit
import noise #https://github.com/caseman/noise/archive/refs/heads/master.zip
import vec_noise
import cv2
import numpy as np


np.random.seed(123)

s1 = np.zeros((1000,1000))
s2 = np.zeros((1000,1000))
p1 = np.zeros((1000,1000))
p2 = np.zeros((1000,1000))
s3 = np.zeros((1000,1000))

def simplexn():
	for y in range(1000):
		for x in range(1000):
			s1[x][y] = noise.snoise2(x/1000,y/1000) + noise.snoise2(x/10,y/10)/10

def simplexv():
	for y in range(1000):
		for x in range(1000):
			s2[x][y] = vec_noise.snoise2(x/1000,y/1000) + vec_noise.snoise2(x/10,y/10)/10
   
def simplexo():
	for y in range(1000):
		for x in range(1000):
			s3[x][y] = opensimplex.noise2(x/10,y/10)/10

def perlinn():
	for y in range(1000):
		for x in range(1000):
			p1[x][y] = noise.pnoise2(x/1000,y/1000) + noise.pnoise2(x/10,y/10)/10

def perlinv():
	for y in range(1000):
		for x in range(1000):
			p2[x][y] = vec_noise.pnoise2(x/1000,y/1000) + vec_noise.pnoise2(x/10,y/10)/10

if __name__ == '__main__':
	print("Simplex Noise")
	print(timeit.timeit("simplexn()",setup="from __main__ import simplexn",number=1))
	print("Vector Simplex Noise")
	print(timeit.timeit("simplexv()",setup="from __main__ import simplexv",number=1))
	#print("OpenSimplex Noise")
	#print(timeit.timeit("simplexo()",setup="from __main__ import simplexo",number=1))
	print("Perlin Noise")
	print(timeit.timeit("perlinn()",setup="from __main__ import perlinn",number=1))
	print("Vector Perlin Noise")
	print(timeit.timeit("perlinv()",setup="from __main__ import perlinv",number=1))
	cv2.imshow("Simplex Noise",s1)
	cv2.imshow("Vector Simplex Noise",s2)
	cv2.imshow("Perlin Noise",p1)
	cv2.imshow("Vector Perlin Noise",p2)
	cv2.waitKey(0)