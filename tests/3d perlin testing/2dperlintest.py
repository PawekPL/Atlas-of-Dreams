import matplotlib.pyplot as plt
import numpy as np
from perlin_numpy import (
    generate_perlin_noise_2d, generate_fractal_noise_2d
)
noise = generate_perlin_noise_2d((256, 256), (8, 8))
plt.imshow(noise, cmap='gray', interpolation='lanczos')
plt.colorbar()
plt.show()
