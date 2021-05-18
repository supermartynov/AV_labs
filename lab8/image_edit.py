from PIL import Image, ImageDraw
import numpy as np
from matplotlib import pyplot as plt
import math

def greyShades(img):
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

def findParametrs(hist):
   min = 0
   max = 0
   pixelsAmount = hist[0].sum()
   counter = 0
   flag = 0
   mean = 0

   for i in range(len(hist[0])):
      if hist[0][i] > max:
         max = i
      if hist[0][i] > 0 and flag == 0:
         min = i
         flag = 1
      counter += i * hist[0][i]
   mean = counter // pixelsAmount
   return min, max, mean

def create_hist(image):
   img = image
   width = img.size[0]
   height = img.size[1]
   pix = list()
   for i in range(width):
      for j in range(height):
         pixel = img.getpixel((i, j))
         pix.append(pixel)

   hist = plt.hist(pix, range(0, max(pix) + 2))
   return hist

def draw_plot(hist, name):
   fig, axs = plt.subplots(1, 1, figsize=(9, 3))
   axs.bar(np.arange(0, len(hist[0])), height=hist[0])
   plt.savefig(name)

def logarithmic(img, min, max, mean, l):
   width = img.size[0]
   height = img.size[1]
   logImg = Image.new('L', (width, height))
   positiveRange = 0
   negativeRange = 0
   positiveAlpha = 0
   negativeAlpha = 0

   if (max - mean > 2):
      positiveRange = max - mean
   else:
      positiveRange = 2

   if (mean - min > 2):
      negativeRange = mean - min
   else:
      negativeRange = 2

   positiveAlpha = (2 ** l) / math.log(positiveRange)
   negativeAlpha = (2 ** l) / math.log(negativeRange)

   for i in range(width):
      for j in range(height):
         pix = img.getpixel((i, j))
         tmpF = pix - mean
         if (tmpF > 0 ):
            newPix = round(mean + positiveAlpha * math.log(tmpF))
            logImg.putpixel((i, j), newPix)
         if (tmpF < 0 ):
            newPix = round(mean - negativeAlpha * math.log(abs(tmpF)))
            logImg.putpixel((i, j), newPix)
         if (tmpF == mean):
            newPix = mean
            logImg.putpixel((i, j), round(newPix))
   return logImg

def createFiles():
   for i in range(8):
      img = Image.open(f'img/img{i + 1}.jpeg')
      if img.mode == 'L':
         greyImg = img  # greyShades(img)
      else:
         greyImg = greyShades(img)
      hist = create_hist(greyImg)
      draw_plot(hist, f'hists/hist{i + 1}_original')
      min, max, mean = findParametrs(hist)
      newImg = logarithmic(greyImg, min, max, mean, 7)
      new_hist = create_hist(newImg)
      draw_plot(new_hist, f'hists/hist{i + 1}changed')
      newImg.save(f'results/hist{i + 1}_changed.jpeg')

createFiles()


'''img = Image.open('img/stars.png')
greyImg = greyShades(img)
hist = create_hist(greyImg)
min, max, mean = findParametrs(hist)
print(min, max, mean)
newImg = logarithmic(greyImg, min, max, mean, 7)
greyImg.show()
newImg.show()'''