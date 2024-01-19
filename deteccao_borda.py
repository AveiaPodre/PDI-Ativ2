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

def sobel(image):
    image = image.convert('L')
    expanded_image = expand_image(image)

    #máscaras de sobel
    sobel_mask_x = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]])
    sobel_mask_y = np.array([[-1, -2, -1], [0, 0, 0], [1, 2, 1]])

    #inicializa a imagem a ser retornada futuramente
    sobel_x = np.zeros_like(expanded_image, dtype=np.float32)
    sobel_y = np.zeros_like(expanded_image, dtype=np.float32)
    height, width = expanded_image.size

    #aplica a convolução na imagem usando a máscara x
    for i in range(1, height - 1):
        for j in range(1, width - 1):
            patch = expanded_image.crop((j - 1, i - 1, j + 2, i + 2))
            sobel_x[i, j] = np.sum(patch * sobel_mask_x)

    #aplica a convolução na imagem usando a máscara y
    for i in range(1, height - 1):
        for j in range(1, width - 1):
            patch = expanded_image.crop((j - 1, i - 1, j + 2, i + 2))
            sobel_y[i, j] = np.sum(patch * sobel_mask_y)

    #calcula a magnitude
    magnitude = np.sqrt(sobel_x**2 + sobel_y**2)

    # Ajuste do limite dos valores para o intervalo entre [0, 255]
    magnitude = np.clip(magnitude, 0, 255) 

    return magnitude[1:-1, 1:-1]

def prewitt(image):
    image = image.convert('L')
    expanded_image = expand_image(image)

    #máscaras de prewitt
    prewitt_mask_x = np.array([[-1, -1, -1], [0, 0, 0], [1, 1, 1]])
    prewitt_mask_y = np.array([[-1, 0, 1], [-1, 0, 1], [-1, 0, 1]])

    #inicializa a imagem a ser retornada futuramente
    prewitt_x = np.zeros_like(expanded_image, dtype=np.float32)
    prewitt_y = np.zeros_like(expanded_image, dtype=np.float32)
    height, width = expanded_image.size

    #aplica a convolução na imagem usando a máscara x
    for i in range(1, height - 1):
        for j in range(1, width - 1):
            patch = expanded_image.crop((j - 1, i - 1, j + 2, i + 2))
            prewitt_x[i, j] = np.sum(patch * prewitt_mask_x)

    #aplica a convolução na imagem usando a máscara y
    for i in range(1, height - 1):
        for j in range(1, width - 1):
            patch = expanded_image.crop((j - 1, i - 1, j + 2, i + 2))
            prewitt_y[i, j] = np.sum(patch * prewitt_mask_y)

    #calcula a magnitude
    magnitude = np.sqrt(prewitt_x**2 + prewitt_y**2)

    # Ajuste do limite dos valores para o intervalo entre [0, 255]
    magnitude = np.clip(magnitude, 0, 255) 

    return magnitude[1:-1, 1:-1]

#carrega a imagem original a ser manipulada
lena = Image.open('lena_gray.bmp')

#faz uso do filtro de sobel, salva a imagem e prepara para plotagem
lena_sobel_array = sobel(lena)
lena_sobel_image = Image.fromarray(lena_sobel_array)
lena_sobel_image = lena_sobel_image.convert('L')
lena_sobel_image.save('lena_sobel.bmp')
plt.subplot(1, 3, 1)
plt.imshow(np.array(lena_sobel_image), cmap='gray')
plt.title('Filtro de Sobel')

#faz uso do filtro de prewitt, salva a imagem e prepara para plotagem
lena_prewitt_array = prewitt(lena)
lena_prewitt_image = Image.fromarray(lena_prewitt_array)
lena_prewitt_image = lena_prewitt_image.convert('L')
lena_prewitt_image.save('lena_prewitt.bmp')
plt.subplot(1, 3, 2)
plt.imshow(np.array(lena_prewitt_image), cmap='gray')
plt.title('Filtro de Prewitt')

#cálculo e plotagem da diferença dos dois processos
lena_difference = lena_sobel_array - lena_prewitt_array
lena_difference = np.clip(lena_difference, 0, 255)
lena_difference = Image.fromarray(lena_difference)
lena_difference =  lena_difference.convert('L')
lena_difference.save('lena_difference.bmp')
plt.subplot(1, 3, 3)
plt.imshow(np.array(lena_difference), cmap='gray')
plt.title('Sobel X Prewitt')

#plota as duas imagens geradas
plt.tight_layout()
plt.show()

