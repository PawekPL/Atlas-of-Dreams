import numpy as np
def find_nearest(array, value):
    array = np.asarray(array)
    print(np.where(np.abs(array - value)==np.abs(array - value).min()))
    idx = np.where(np.abs(array - value)==np.abs(array - value).min())
    return array[idx]

array = np.array([[60,1,-0.2,1,1],[60,1,1,1,1],[60,0,0,0,0],[90,-1,-1,-1,-1]])
print(array)
# [ 0.21069679  0.61290182  0.63425412  0.84635244  0.91599191  0.00213826
#   0.17104965  0.56874386  0.57319379  0.28719469]

value = [60,1,1,1,1]

print(array)

print(find_nearest(array, value))
