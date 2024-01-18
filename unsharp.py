import numpy as np
import matplotlib.pyplot as plt
from PIL import Image, ImageFilter

def unsharp_masking(image, k=1, radius=1):
    image = image.convert("L")

    # Aplicação do filtro gaussiano na imagem
    blurred_image = image.filter(ImageFilter.GaussianBlur(radius=radius))
    
    # Converte as imagens para arrays NumPy
    image_array = np.array(image, dtype=float)
    blurred_image_array = np.array(blurred_image, dtype=float)

    # Subtração da imagem borrada pela original
    difference = image_array - blurred_image_array

    # Multiplicação da diferença obtida pelo fator e então soma-se à imagem original
    sharpened_array = image_array + k * difference

    # Ajuste do limite dos valores para o intervalo entre [0, 255] e conversão novamente para imagem
    sharpened_array = np.clip(sharpened_array, 0, 255) 
    sharpened_image = Image.fromarray(sharpened_array.astype(np.uint8))
    
    return sharpened_image

lena = Image.open('lena_gray.bmp')
lena_unsharp = unsharp_masking(lena)
lena_unsharp.save('lena_unsharp.bmp')

plt.imshow(lena_unsharp, cmap='gray')
plt.show()
