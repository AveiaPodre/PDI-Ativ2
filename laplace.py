import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from expand import expand_image

def laplace(image):
    mask = np.array([[-1, -1, -1],
                       [-1, 8, -1],
                       [-1, -1, -1]])
    
    #expande imagem em um pixel de espessura
    expanded_image = expand_image(image)

    #inicializa a imagem a ser retornada futuramente
    result = np.zeros_like(expanded_image, dtype=np.float32)
    height, width = expanded_image.size

    #aplica a convolução na imagem usando a máscara
    for i in range(1, height - 1):
        for j in range(1, width - 1):
            patch = expanded_image.crop((j - 1, i - 1, j + 2, i + 2))
            result[i, j] = np.sum(patch * mask)

    #converte o array desejado em uma imagem em escala de cinza
    result = Image.fromarray(result[1:-1, 1:-1])
    result = result.convert('L')

    return result

lena = Image.open("lena_gray.bmp")
lena_laplace = laplace(lena)
lena_laplace.save('lena_laplace.bmp')

plt.imshow(lena_laplace, cmap='gray')
plt.show()

