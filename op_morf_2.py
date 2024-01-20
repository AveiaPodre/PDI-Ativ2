from PIL import Image
import numpy as np
import matplotlib.pyplot as plt

def dilation(image, struct_element, center):
    height, width = image.size
    img_array = np.array(image)

    #inicializa a imagem resultado
    dilated_image = Image.new("L", (height, width), color=0)

    for x in range(height):
        for y in range(width):
            if img_array[y, x] > 0:
                #aplica dilatação
                for i in range(struct_element.shape[0]):
                    for j in range(struct_element.shape[1]):
                        nx, ny = x + i - center[0], y + j - center[1]
                        if 0 <= nx < height and 0 <= ny < width:
                            dilated_image.putpixel((nx, ny), 255)

    return dilated_image

def erosion(image, struct_element, center):
    height, width = image.size
    img_array = np.array(image)

    #inicializa a imagem resultado
    eroded_image = Image.new("L", (height, width), color=0)

    for x in range(height):
        for y in range(width):
            #aplica erosão
            for i in range(struct_element.shape[0]):
                for j in range(struct_element.shape[1]):
                    nx, ny = x + i - center[0], y + j - center[1]
                    if 0 <= nx < height and 0 <= ny < width:
                        if struct_element[i, j] > 0 and img_array[ny, nx] == 0:
                            break
                else:
                    #se nenhum pixel de background foi encontrado
                    eroded_image.putpixel((x, y), 255)

    return eroded_image

def opening(image, struct_element, center):
    #aplica abertura(erosão seguida de dilatação)
    opened_image = erosion(image, struct_element, center)
    opened_image = dilation(opened_image, struct_element, center)
    return opened_image

def closing(image, struct_element, center):
    #aplica fechamento(dilatação seguida de erosão)
    closed_image = dilation(image, struct_element, center)
    closed_image = erosion(closed_image, struct_element, center)
    return closed_image

struct_element = np.array([[0, 1, 0],
                           [1, 1, 1],
                           [0, 1, 0]])
center = (1, 1)