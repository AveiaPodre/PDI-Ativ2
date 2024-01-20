import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

#op: 0-união, 1-interseção, 2-diferença
def op_morf(imA, imB, op):
    imA = imA.convert('L')
    imB = imB.convert('L')

    array_a = np.array(imA)
    array_b = np.array(imB)

    if(op == 0):
        result = np.maximum(array_a, array_b)
    elif(op == 1):
        result = np.minimum(array_a, array_b)
    elif(op == 2):
        result = np.zeros_like(array_a)
        width, height = result.shape

        for i in range(width):
            for j in range(height):
                result[i,j] = max(int(array_a[i,j] - array_b[i,j]), 0)
    else:
        raise ValueError("Input não identificado")
    
    result = Image.fromarray(result)

    return result