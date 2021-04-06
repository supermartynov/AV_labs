from PIL import Image, ImageDraw, ImageFont
import numpy as np
from matplotlib import pyplot as plt
import csv
from Otsu_binarization import Otsu_binarization
from statistics import mean
import time

ALPHABET = 'AӘБВГҒДЕЁЖЗИЙКҚЛМНҢОӨПРСТУҰҮФХҺЦЧШЩЪЫІЬЭЮЯ'

def renameFiles():
    for i in range(42):
        img = Image.open('казахские черные/' + str(i + 1) + '.png')
        img.save('казахские черные/' + ALPHABET[i] + '.png')


def getParametrs(img):
    img = Image.open(img)
    width = img.size[0]
    height = img.size[1]
    size = width * height
    weight_black, normal_black, x_center, y_center = 0, 0, 0, 0

    for i in range(width):
        for j in range(height):
            if img.getpixel((i, j)) == 0:
                weight_black += 1
                x_center += i
                y_center += j

    normal_black = weight_black / size
    x_center = x_center // weight_black
    x_norm_center = (x_center - 1) // (width - 1)
    y_center = y_center // weight_black
    y_norm_center = (y_center - 1) // (height - 1)

    return [weight_black, normal_black, x_center, y_center, x_norm_center, y_norm_center]

def getMomentParametrs(img, x_center, y_center):
    img = Image.open(img)
    width = img.size[0]
    height = img.size[1]

    for i in range(width):
        for j in range(height):
            if img.getpixel((i, j)) == 0:
                x_moment = ((j - x_center) ** 2)
                y_moment = ((i - y_center) ** 2)

    size = width ** 2 + height ** 2
    x_norm_moment = x_moment / size
    y_norm_moment = y_moment / size

    return [x_moment, x_norm_moment, y_moment, y_norm_moment]

'''def getProfil(img):
    img = Image.open(img)
    width = img.size[0]
    height = img.size[1]
    y_profil = np.array([])
    x_profil = np.array([])
    black = 0

    for i in range(width):
        black = 0
        for j in range(height):
            if img.getpixel((i, j)) == 0:
                black += 1
        y_profil = np.append(y_profil, black)


    for i in range(height):
        black = 0
        for j in range(width):
            if img.getpixel((i, j)) == 0:
                black += 1
        x_profil = np.append(x_profil, black)

    return x_profil, y_profil'''

def getProfil(file):
    img = Image.open(file)
    width = img.size[0]
    height = img.size[1]
    x_profiles = []
    y_profiles = []

    for x in range(width):
        pix = 0
        for y in range(height):
            if img.getpixel((x, y)) == 0:
                pix += 1
        x_profiles.append(pix)

    for y in range(height):
        pix = 0
        for x in range(width):
            if img.getpixel((x, y)) == 0:
                pix += 1
        y_profiles.append(pix)

    return [x_profiles, y_profiles]


def get_hist_profile(s):
    for c in s:
        x_profile, y_profile = getProfil("казахские черные/" + c + '.png')
        fig, axs = plt.subplots(1, 2, figsize=(9, 3))

        axs[0].bar(np.arange(0, len(x_profile)), height=x_profile)
        axs[0].set_ybound(upper=52)
        axs[0].set_title('Х профиль')
        axs[1].barh(np.arange(0, len(y_profile)), width=y_profile)
        axs[1].set_xbound(upper=60)
        axs[1].set_title('Y профиль')
        plt.savefig(f'hists/{c}.png', dpi=70)
        del fig
        del axs


def makeCSV():
    with open("letters_info.csv", 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=";")
        writer.writerow(["Символ", "Вес", "Удельный вес", "Координата центра тяжести x",
                         "Координата центра тяжести y",  "Нормированная координата центра тяжести x",
                         "Нормированная координата центра тяжести y", "Осевой момент инерции по x",
                         "Нормированный осевой момент инерции по x", "Осевой момент инерции по  y",
                         "Нормированный осевой момент инерции по y"])

        for s in ALPHABET:
            weight_black, normal_black, x_center, y_center, x_norm_center, y_norm_center = getParametrs('казахские черные/' + s + '.png')
            x_moment, x_norm_moment, y_moment, y_norm_moment = getMomentParametrs('казахские черные/' + s + '.png', x_center, y_center)
            writer.writerow([s, str(weight_black), str(normal_black), str(x_center), str(y_center), str(x_norm_center), str(y_norm_center), str(x_moment),
                             str(x_norm_moment), str(y_moment), str(y_norm_moment)])


#renameFiles()
#get_hist_profile(ALPHABET)
#makeCSV()
Otsu_binarization('казахская.png').save('казахская_чб.png')