import numpy as np
from scipy import spatial

array = np.array([[0,1,-0.2,1,1,0],[0,1,1,1,1,0],[.1,0,0,0,0,0],[.3,-1,-1,-1,-1,0],[.1,-0.55,.4567,1,0,0],[.1,-0.55,.4567,1,0,.02],[-0.1,-0.55,.4567,1,0,.01]])
print(array)
# [ 0.21069679  0.61290182  0.63425412  0.84635244  0.91599191  0.00213826
#   0.17104965  0.56874386  0.57319379  0.28719469]


value = np.random.random(6)

tree = spatial.cKDTree(array)
_,id=tree.query(value)

print(value)
print(array[id])
