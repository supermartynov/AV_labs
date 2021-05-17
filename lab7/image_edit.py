from PIL import Image

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





def createHarlic(img):

    width = img.width
    height = img.height
    size = width * height
    k = 0
    anotherK = 4 * width * height - (4 * width * height - 4 * (width - 6) * (height - 6))
    maxEL = 0

    HarlicMatrix = []
    for i in range(256):
        HarlicMatrix.append([0] * 256)


    for i in range(3, width - 3):
        for j in range(3,height - 3):
            centerPix = img.getpixel((i, j))
            pix45 = img.getpixel((i + 3, j + 3))
            pix135 = img.getpixel((i - 3, j + 3))
            pix225 = img.getpixel((i - 3, j - 3))
            pix315 = img.getpixel((i + 3, j - 3))
            HarlicMatrix[centerPix][pix45] += 1
            HarlicMatrix[centerPix][pix135] += 1
            HarlicMatrix[centerPix][pix225] += 1
            HarlicMatrix[centerPix][pix315] += 1

    for i in range(256):
        for j in range(256):
            if HarlicMatrix[i][j] > maxEL:
                maxEL = HarlicMatrix[i][j]
    thirdK = maxEL // 255

    for i in range(256):
        for j in range(256):
            k += HarlicMatrix[i][j]


    for i in range(256):
        for j in range(256):
            HarlicMatrix[i][j] = HarlicMatrix[i][j] // thirdK

    print(thirdK)

    return HarlicMatrix


img1 = Image.open('img1/img2.png')
img_grey = image_grey_shades_for_threshold(img1)
Matrix = createHarlic(img_grey)

sum = 0
for i in range(256):
    for j in range(256):
        if Matrix[i][j] > 0:
            print(i, j, Matrix[i][j])
