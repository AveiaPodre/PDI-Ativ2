import numpy as np
import matplotlib.pyplot as plt
from PIL import Image, ImageFilter

def highboost(image, k=2):
    image = image.convert('L')

    # Aplicação do filtro passa-baixa (suavização)
    low_pass = image.filter(ImageFilter.GaussianBlur(5))

    # Converte as imagens para arrays NumPy
    image_array = np.array(image, dtype=float)
    low_pass_array = np.array(low_pass, dtype=float)

    # Cálculo da imagem passa-alta (componentes de alta frequência)
    high_pass = image_array - low_pass_array

    # Aplicação do fator de realce
    enhanced_image = image_array + k * high_pass

    # Ajuste do limite dos valores para o intervalo entre [0, 255] e conversão novamente para imagem
    enhanced_image = np.clip(enhanced_image, 0, 255).astype(np.uint8)
    enhanced_image = Image.fromarray(enhanced_image)

    return enhanced_image

lena = Image.open('lena_gray.bmp')
lena_highboost = highboost(lena)
lena_highboost.save('lena_highboost.bmp')

plt.imshow(np.array(lena_highboost), cmap='gray')
plt.show()