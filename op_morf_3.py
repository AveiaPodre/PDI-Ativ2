from PIL import Image
import numpy as np
import cv2
from scipy.spatial import ConvexHull
import matplotlib.pyplot as plt

red = (255, 0, 0, 255)
green = (0, 255, 0, 255)
blue = (0, 0, 255, 255)
yellow = (255, 255, 0, 255)
white = (255, 255, 255, 255)
black = (0, 0, 0, 255)
target_colors = [blue, green, yellow]

def extract(image, color, bg=white):
    width, height = image.size

    #inicialização da nova imagem com o fundo desejado
    result = Image.new(image.mode,(width, height), bg)

    for i in range(width):
        for j in range(height):
            pixel_color = image.getpixel((i, j))

            if(pixel_color == color):
                result.putpixel((i, j), color)

    return result

def exclude(image, color, bg=white):
    width, height = image.size

    #inicialização da nova imagem como cópia da original
    result = image.copy()

    for i in range(width):
        for j in range(height):
            pixel_color = image.getpixel((i, j))

            if(pixel_color == color):
                result.putpixel((i, j), bg)

    return result

def flood_fill(image, new_color, old_color=white, x=0, y=0):
    width, height = image.size
    
    #verifica se as coordenadas estão dentro dos limites da imagem
    if x < 0 or x >= width or y < 0 or y >= height:
        return
    
    #obtém a cor do pixel atual
    pixel_color = image.getpixel((x, y))
    
    #verifica se a cor do pixel atual é igual à cor original
    if pixel_color == old_color:
        #pinta o pixel com a nova cor
        image.putpixel((x, y), new_color)
        
        # Chama recursivamente para os vizinhos
        flood_fill(image, new_color, old_color, x+1, y)
        flood_fill(image, new_color, old_color, x-1, y)
        flood_fill(image, new_color, old_color, x, y+1)
        flood_fill(image, new_color, old_color, x, y-1)

def iter_flood_fill(image, new_color, old_color=white, x=0, y=0):
    width, height = image.size
    
    # Check if coordinates are within the image boundaries
    if x < 0 or x >= width or y < 0 or y >= height:
        return
    
    # Create a stack for iterative approach
    stack = [(x, y)]
    
    while stack:
        current_x, current_y = stack.pop()
        
        # Check if the current pixel has the old color
        if image.getpixel((current_x, current_y)) == old_color:
            # Paint the pixel with the new color
            image.putpixel((current_x, current_y), new_color)
            
            # Add neighboring pixels to the stack
            if current_x + 1 < width:
                stack.append((current_x + 1, current_y))
            if current_x - 1 >= 0:
                stack.append((current_x - 1, current_y))
            if current_y + 1 < height:
                stack.append((current_x, current_y + 1))
            if current_y - 1 >= 0:
                stack.append((current_x, current_y - 1))

def hole_fill(image_origin, image_flood, fill_color, hole_color=white):
    width, height = image_origin.size

    #inicializa a imagem resultado como cópia da original
    result = image_origin.copy()

    for i in range(width):
        for j in range(height):
            flood_pixel_color = image_flood.getpixel((i, j))

            if (flood_pixel_color == hole_color):
                result.putpixel((i, j), fill_color)
    
    return result

def hole_fill_process(image, color):
    extracted_image = extract(image, color)
    iter_flood_fill(extracted_image, color)
    result = hole_fill(image, extracted_image, color)

    return result

quadro = Image.open('quadro.png')

""" black_fill
black_fill = hole_fill_process(quadro, black)
black_fill.save('black_fill.png')
plt.imshow(black_fill, cmap='gray')
plt.show()
"""

""" black_exclude
black_exclude = exclude(quadro, black)
black_exclude.save('black_exclude.png')
plt.imshow(black_exclude, cmap='gray')
plt.show()
"""


blue_fill = hole_fill_process(quadro, blue)
blue_green_fill = hole_fill_process(blue_fill, green)
blue_green_yellow_fill = hole_fill_process(blue_green_fill, yellow)
color_fill = blue_green_yellow_fill

"""
color_fill.save('color_fill.png')
plt.imshow(color_fill, cmap='gray')
plt.show()
"""

