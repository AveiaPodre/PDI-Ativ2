import numpy as np
import matplotlib.pyplot as plt
from PIL import Image, ImageFilter

def unsharp_masking(image, k=1.5, radius=1):
    image = image.convert("L")
    
    #aplicação do filtro gaussiano na imagem
    blurred_image = image.filter(ImageFilter.GaussianBlur(radius=radius))
    
    #subtração da imagem borrada pela original
    difference = np.array(image) - np.array(blurred_image)
     
    #multiplicação da diferença obtida pelo fator e então soma-se à imagem original
    sharpened_array = np.array(image) + k * difference

    #ajuste do limite dos valores para o intervalo entre [0,255] e converte novamente para imagem
    sharpened_array = np.clip(sharpened_array, 0, 255) 
    sharpened_image = Image.fromarray(sharpened_array.astype(np.uint8))
    
    return sharpened_image

lena = Image.open('lena_gray.bmp')
lena_unsharp = unsharp_masking(lena)
lena_unsharp.save('lena_unsharp.bmp')

plt.imshow(lena_unsharp, cmap='gray')
plt.show()
