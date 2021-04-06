from PIL import Image, ImageDraw
import numpy as np
import time

def image_grey_shades(image):

   width = img.size[0]
   height = img.size[1]
   grey_img = Image.new('L', (width, height))

   for i in range(width):
      for j in range(height):
         pixel = img.getpixel((i, j))
         sr = 0
         for color in pixel:
            sr += color // 3
            grey_img.putpixel((i, j), (sr))
   return grey_img

def output_matrix(matrix):
    for i in range(len(matrix)):
        print(matrix[i])
        print("\n")

def Sharr_get_matrix(img):
    width = img.size[0]
    height = img.size[1]
    G_x = list()
    G_y = list()
    G = list()
    G_norm = list()
    G_max = 0
    row_x = list()
    row_y = list()
    row = list()

    for i in range(2, width - 2):

        if len(row_x) != 0:
            G_x.append(row_x)

        if len(row_y) != 0:
            G_y.append(row_y)

        if len(row) != 0:
            G.append(row)

        row_x = list()
        row_y = list()
        row = list()

        for j in range(2, height - 2):
            G_x_element = 10 * img.getpixel((i - 1, j)) - 10 * img.getpixel((i + 1, j)) + \
                            3 * img.getpixel((i - 1, j + 1)) - 3 * img.getpixel((i + 1, j - 1)) + 3 * img.getpixel(
                             (i - 1, j - 1)) - 3 * img.getpixel((i + 1, j + 1))
            G_y_element = (-10 * img.getpixel((i, j - 1))) + 10 * img.getpixel(
                            (i, j + 1)) + 3 * img.getpixel((i - 1, j + 1)) - 3 * img.getpixel((i + 1, j - 1)) - 3 * img.getpixel(
                             (i - 1, j - 1)) + 3 * img.getpixel((i + 1, j + 1))
            G_element = abs(G_x_element) + abs(G_y_element)

            if (G_max < G_element):
                G_max = G_element


            row_x.append(G_x_element)
            row_y.append(G_y_element)
            row.append(G_element)


    G_norm_row = list()

    for i in range(len(G)):
        if (len(G_norm_row) != 0):
             G_norm.append(G_norm_row)
        G_norm_row = list()
        for j in range(len(G[0])):
            G_norm_row.append(int((G[i][j] * 255) / G_max))

    return G_x, G_y, G, G_norm

def Matrix_image(G):
    width = len(G)
    height = len(G[1])
    G_max = 0;
    img = Image.new('L', (width, height))

    for i in range(width):
        for j in range(height):
            if(G_max < G[i][j]):
                G_max = G[i][j]


    for i in range(width):
        for j in range(height):
            pixel = G[i][j] * 255 //G_max
            img.putpixel((i, j), pixel)
    return img


def Sharr_image(G_norm, t):
    width = len(G_norm)
    height = len(G_norm[1])
    img = Image.new('L', (width, height))

    for i in range(width):
        for j in range(height):
            if G_norm[i][j] > t:
                img.putpixel((i, j), 255)
            else:
                img.putpixel((i, j), 0)
    return img


#img = Image.open('smile.png').convert('RGB')
img = Image.open('двигатель.jpg')
img_grey = image_grey_shades(img)
'''img_grey.save('двигатель_grey.jpg')
matrix = Sharr_get_matrix(img_grey)[0]
Matrix_image(matrix).save('двигатель_X.jpg')
matrix = Sharr_get_matrix(img_grey)[1]
Matrix_image(matrix).save('двигатель_Y.jpg')
matrix = Sharr_get_matrix(img_grey)[2]
Matrix_image(matrix).save('двигатель_G.jpg')'''
matrix = Sharr_get_matrix(img_grey)[3]
Sharr_image(matrix, 45).save('двигатель_45.jpg')






