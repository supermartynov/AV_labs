from PIL import Image, ImageDraw, ImageFont
import numpy as np
from operator import itemgetter
from matplotlib import pyplot as plt
import csv
from helper import easyBin, getProfil, findLetters, textFinder


ALPHABET = 'AӘБВГҒДЕЁЖЗИЙКҚЛМНҢОӨПРСТУҰҮФХҺЦЧШЩЪЫІЬЭЮЯ'


def Features(img):
    width = img.width
    height = img.height
    size = width * height
    weight_black, normal_black, x_center, y_center = 0, 0, 0, 0

    for i in range(width):
        for j in range(height):
            if img.getpixel((i, j)) == 0:
                weight_black += 1
                x_center += i
                y_center += j

    normal_black = weight_black / size
    x_center = x_center / weight_black
    x_norm_center = (x_center - 1) / (width - 1)
    y_center = y_center / weight_black
    y_norm_center = (y_center - 1) / (height - 1)

    return [weight_black, normal_black, x_center, y_center, x_norm_center, y_norm_center]


def AxialMomentFeatures(img, x_center, y_center, weight_black):
    width = img.width
    height = img.height
    x_moment = 0
    y_moment = 0
    I45_center = 0
    I135_center = 0

    for i in range(width):
        for j in range(height):
            if img.getpixel((i, j)) == 0:
                x_moment += ((j - x_center) ** 2)
                y_moment += ((i - y_center) ** 2)
                I45_center += ((j - y_center - i + x_center) ** 2) / 2
                I135_center += ((j - y_center + i - x_center) ** 2) / 2

    x_moment = x_moment / weight_black
    y_moment = y_moment / weight_black
    M_N = width ** 2 + height ** 2
    x_norm_moment = x_moment / M_N
    y_norm_moment = y_moment / M_N
    I45_rel = I45_center / (weight_black ** 2)
    I135_rel = I135_center / (weight_black ** 2)

    return [x_moment, x_norm_moment, y_moment, y_norm_moment, I45_rel, I135_rel]

def FindDistance(realFile, idealFile):
    idealFeatures = Features(idealFile)
    realFeatures = Features(realFile)
    axialRealFeatures = AxialMomentFeatures(realFile, realFeatures[2], realFeatures[3], realFeatures[0])
    axialIdealFeatures = AxialMomentFeatures(idealFile, idealFeatures[2], idealFeatures[3], idealFeatures[0])
    print(idealFeatures)
    print(realFeatures)
    print(axialIdealFeatures)
    print(axialRealFeatures)


    distance = ((idealFeatures[4] - realFeatures[4]) ** 2
               + (idealFeatures[1] - realFeatures[1]) ** 2 + (idealFeatures[5] - realFeatures[5]) ** 2
               + (axialRealFeatures[1] - axialIdealFeatures[1]) ** 2
                + (axialIdealFeatures[3] - axialIdealFeatures[3]) ** 2) ** (1/2)

    return distance




def makeCSV():
    with open("letters_info_ы_слитно.csv", 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=";")
        writer.writerow(["Символ", "Дистанции"])
        for i in range(25):
            tmpStr = ''
            mas =[]
            realImg = Image.open('results_cropped/' + str(i) + '.png')
            for j in range(42):
                idealImg = Image.open('алфавит/' + ALPHABET[j] + '.png')
                mas.append([round(FindDistance(realImg, idealImg), 3), ALPHABET[j]])
                mas.sort()
            for j in range(42):
                tmpStr += mas[j][1] + " - " + str(mas[j][0]) + ' '
            writer.writerow([str(i + 1), tmpStr])








'''img = Image.open('строки/строка_2.png')
easyBin(img, 220).save('строка1_чб.png')
x_profil = getProfil('строка1_чб.png')[0]
y_profil = getProfil('строка1_чб.png')[1]
top_coord, bottom_coord, left_coord, right_coord = textFinder(x_profil, y_profil)
img = Image.open('строка1_чб.png')
findLetters(img, x_profil, y_profil, 0)'''
img1 = Image.open('results_cropped/0.png', )
img2 = Image.open('алфавит/Д.png')
FindDistance(img1, img2)


#makeCSV()