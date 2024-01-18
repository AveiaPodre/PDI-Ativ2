import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

def expand_image(image):
    # Obtém as dimensões originais da imagem
    width, height = image.size
    
    # Cria uma nova imagem expandida com uma borda de um pixel
    expanded_image = Image.new('L', (width + 2, height + 2))
    
    # Copia os pixels da imagem original para o centro da imagem expandida
    expanded_image.paste(image, (1, 1, width + 1, height + 1))
    
    # Preenche as bordas superior e inferior com os pixels da primeira e última linha, respectivamente
    expanded_image.paste(image.crop((0, 0, width, 1)), (1, 0, width + 1, 1))
    expanded_image.paste(image.crop((0, height - 1, width, height)), (1, height + 1, width + 1, height + 2))
    
    # Preenche as bordas esquerda e direita com os pixels da primeira e última coluna, respectivamente
    expanded_image.paste(image.crop((0, 0, 1, height)), (0, 1, 1, height + 1))
    expanded_image.paste(image.crop((width - 1, 0, width, height)), (width + 1, 1, width + 2, height + 1))
    
    # Preenche os cantos com os valores dos cantos originais
    expanded_image.paste(image.crop((0, 0, 1, 1)), (0, 0, 1, 1))
    expanded_image.paste(image.crop((width - 1, 0, width, 1)), (width + 1, 0, width + 2, 1))
    expanded_image.paste(image.crop((0, height - 1, 1, height)), (0, height + 1, 1, height + 2))
    expanded_image.paste(image.crop((width - 1, height - 1, width, height)), (width + 1, height + 1, width + 2, height + 2))
    
    return expanded_image

def laplace(image):
    mask = np.array([[-1, -1, -1],
                       [-1, 8, -1],
                       [-1, -1, -1]])
    
    #expande imagem em um pixel de espessura
    expanded_image = expand_image(image)

    #inicializa a imagem a ser retornada futuramente
    result = np.zeros_like(expanded_image, dtype=np.float32)
    height, width = expanded_image.size

    for i in range(1, height - 1):
        for j in range(1, width - 1):
            patch = expanded_image.crop((j - 1, i - 1, j + 2, i + 2))
            result[i, j] = np.sum(patch * mask)

    return result[1:-1, 1:-1]

lena = Image.open("lena_gray.bmp")
lena_laplace = laplace(lena)

lena_laplace = Image.fromarray(lena_laplace)
lena_laplace = lena_laplace.convert('L')
lena_laplace.save('lena_laplace.bmp')

plt.imshow(lena_laplace, cmap='gray')
plt.show()

