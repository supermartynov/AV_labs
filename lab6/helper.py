from PIL import Image, ImageDraw, ImageFont
import numpy as np
from matplotlib import pyplot as plt
import csv

ALPHABET = 'AӘБВГҒДЕЁЖЗИЙКҚЛМНҢОӨПРСТУҰҮФХҺЦЧШЩЪЫІЬЭЮЯ'


def image_grey_shades_for_threshold(img):
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

def easyBin(img, threshold):
    img = image_grey_shades_for_threshold(img)
    width = img.size[0]
    height = img.size[1]
    new_img = Image.new((img.mode), (width, height))

    for i in range(width):
        for j in range(height):
            if img.getpixel((i, j)) < threshold:
                new_img.putpixel((i, j), 0)
            else:
                new_img.putpixel((i, j), 255)

    return new_img

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

def textFinder(x_profile, y_profile):
    height = len(x_profile)
    width = len(y_profile)
    top_coord = 0
    bottom_coord = 0
    left_coord = 0
    right_coord = 0

    for j in reversed(range(width)):
        if bottom_coord == 0:
            if y_profile[j] < 2:
                continue
            else:
                bottom_coord = j
    for j in range(width):
        if top_coord == 0:
            if y_profile[j] < 2:
                continue
            else:
                top_coord = j

    for i in range(height):
        if left_coord == 0:
            if x_profile[i] < 2:
                continue
            else:
                left_coord = i
                break

    for i in reversed(range(height)):
        if right_coord == 0:
            if x_profile[i] > 0:
                right_coord = i
            else:
                continue

    return bottom_coord, top_coord, left_coord, right_coord


def drawTextFrame(pict, top_coord, bottom_coord, left_coord, right_coord):
    line_lenght = right_coord - left_coord
    vertical_line_length = top_coord - bottom_coord
    framed_image = pict.copy()

    for i in range(left_coord, line_lenght, 3):
        framed_image.putpixel((i, top_coord), 0)
        framed_image.putpixel((i, bottom_coord), 0)

    for j in range(bottom_coord, top_coord, 3):
        framed_image.putpixel((left_coord, j), 0)
        framed_image.putpixel((left_coord - 1, j), 0)
        framed_image.putpixel((right_coord, j), 0)
        framed_image.putpixel((right_coord + 1, j), 0)

    return framed_image


def findLetters(img, x_profil, y_profil, ep):
    bounds = []
    step = 0
    top_coord, bottom_coord, left_coord, right_coord = textFinder(x_profil, y_profil)
    counter = 0

    for i in range(len(x_profil)):
        if x_profil[i] == 0:
           step = 0
        else:
            step += 1
            right_bound = i
            left_bound = right_bound - step
            if x_profil[i + 1] == 0:
                bounds.append((left_bound, right_bound))


    for i in range(len(bounds) - 1):
        left_bound, right_bound = bounds[i]
        left_next_bound, right_next_bound = bounds[i + 1]
        if abs(left_next_bound - right_bound) <= ep:
            counter += 1
            '''bounds.pop(i + 1)
            bounds[i] = (left_bound, right_next_bound)'''
    for i in range(counter):
        for i in range(len(bounds) - 1):
            left_bound, right_bound = bounds[i]
            left_next_bound, right_next_bound = bounds[i + 1]
            if abs(left_next_bound - right_bound) <= ep:
                print(left_next_bound - right_bound)
                bounds.pop(i + 1)
                bounds[i] = (left_bound, right_next_bound)
                break

    for i in range(len(bounds)):
        left_bound, right_bound = bounds[i]
        new_im = img.crop((left_bound, bottom_coord, right_bound + 2, top_coord))
        new_im.save("results/" + str(i) + '.png')

    for i in range(len(bounds)):
        x_pr, y_pr = getProfil('results/' + str(i) + '.png')
        img = Image.open('results/' + str(i) + '.png')
        top, bottom, left, right = textFinder(x_pr, y_pr)
        new_im = img.crop((left, bottom, right + 2, top))
        new_im.save("results_cropped/" + str(i) + '.png')

    return bounds




def get_all_hists():
    for i in range(14):
        x_profile, y_profile = getProfil('results_cropped/'+str(i)+'.png')
        fig, axs = plt.subplots(1, 2, figsize=(9, 3))
        axs[0].bar(np.arange(0, len(x_profile)), height=x_profile)
        # axs[0].set_ybound(upper=52)
        axs[0].set_title('Х профиль')
        axs[1].barh(np.arange(0, len(y_profile)), width=y_profile)
        # axs[1].set_xbound(upper=60)
        axs[1].set_title('Y профиль')
        plt.savefig('letters_hists/' + str(i) + '.png', dpi=70)
        del fig
        del axs


'''def makeCSV():
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
                             str(x_norm_moment), str(y_moment), str(y_norm_moment)])'''
