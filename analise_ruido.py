import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from expand import expand_image

def mediana(image):
    #expande imagem em um pixel de espessura
    expanded_image = expand_image(image)

    #inicializa a imagem a ser retornada futuramente
    result = np.zeros_like(expanded_image, dtype=np.float32)
    height, width = expanded_image.size

    #converte imagem em array
    expanded_image = np.array(expanded_image)

    for i in range(1, height - 1):
        for j in range(1, width - 1):
            neighborhood = []
            neighborhood.append(expanded_image[i-1, j-1])
            neighborhood.append(expanded_image[i-1, j])
            neighborhood.append(expanded_image[i-1, j+1])
            neighborhood.append(expanded_image[i, j-1])
            neighborhood.append(expanded_image[i, j])
            neighborhood.append(expanded_image[i, j+1])
            neighborhood.append(expanded_image[i+1, j-1])
            neighborhood.append(expanded_image[i+1, j])
            neighborhood.append(expanded_image[i+1, j+1])

            neighborhood.sort()
            result[i,j] = neighborhood[4]

    result = np.clip(result, 0, 255).astype(np.uint8)

    return result[1:-1, 1:-1]

def filtragem(image, mask):    
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

    result = np.clip(result, 0, 255).astype(np.uint8)

    return result[1:-1, 1:-1]

lena_ruido = Image.open('lena_ruido.bmp')

#aplicação do filtro de mediana à imagem com ruído
lena_mediana = mediana(lena_ruido)
lena_mediana = Image.fromarray(lena_mediana)
lena_mediana = lena_mediana.convert('L')
lena_mediana.save('lena_mediana.bmp')

#aplicação da máscara desejada à imagem com ruído
mask1 = np.array([[0, 1/5, 0],
                [1/5, 1/5, 1/5],
                [0, 1/5, 0]])

mask2 = np.array([[1/9, 1/9, 1/9],
                [1/9, 1/9, 1/9],
                [1/9, 1/9, 1/9]])

mask3 = np.array([[1/32, 3/32, 1/32],
                [3/32, 16/32, 3/32],
                [1/32, 3/32, 1/32]])

mask4 = np.array([[0, 1/8, 0],
                [1/8, 4/8, 1/8],
                [0, 1/8, 0]])

lena_filtered_array_1 = filtragem(lena_ruido, mask1)
lena_filtered_1 = Image.fromarray(lena_filtered_array_1)
lena_filtered_1.save('lena_filter1.bmp')

lena_filtered_array_2 = filtragem(lena_ruido, mask2)
lena_filtered_2 = Image.fromarray(lena_filtered_array_2)
lena_filtered_2.save('lena_filter2.bmp')

lena_filtered_array_3 = filtragem(lena_ruido, mask3)
lena_filtered_3 = Image.fromarray(lena_filtered_array_3)
lena_filtered_3.save('lena_filter3.bmp')

lena_filtered_array_4 = filtragem(lena_ruido, mask4)
lena_filtered_4 = Image.fromarray(lena_filtered_array_4)
lena_filtered_4.save('lena_filter4.bmp')


#plotagem das imagens
plt.subplot(1, 5, 1)
plt.imshow(lena_mediana, cmap='gray')
plt.title('Mediana')

plt.subplot(1, 5, 2)
plt.imshow(lena_filtered_1, cmap='gray')
plt.title('Máscara 1')

plt.subplot(1, 5, 3)
plt.imshow(lena_filtered_2, cmap='gray')
plt.title('Máscara 2')

plt.subplot(1, 5, 4)
plt.imshow(lena_filtered_3, cmap='gray')
plt.title('Máscara 3')

plt.subplot(1, 5, 5)
plt.imshow(lena_filtered_4, cmap='gray')
plt.title('Máscara 4')

plt.show()