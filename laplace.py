import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

def laplace(image):
    filter = np.array([[-1, -1, -1],
                       [-1, 8, -1],
                       [-1, -1, -1]])
    
    resultado = np.zeros_like(image)