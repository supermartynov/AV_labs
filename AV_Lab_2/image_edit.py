from PIL import Image, ImageDraw

def dirty_picture(img):
    width = img.size[0]
    height = img.size[1]
    
    for i in range(1, width, 3):
        for j in range(1, height, 3):
            img.putpixel((i, j), 0)

    return img

def rang(img, k):
    width = img.size[0]
    height = img.size[1]
    result_img = img.copy()

    for i in range(2, width - 2, 1):
        for j in range(2, height - 2, 1):
            if ((img.getpixel((i - 1, j)) + img.getpixel((i + 1, j)) + img.getpixel((i, j - 1)) + img.getpixel(
                    (i, j + 1)) + img.getpixel((i - 1, j - 1)) + img.getpixel((i + 1, j - 1)) + img.getpixel(
                    (i, j + 1)) + img.getpixel((i + 1, j + 1)))//255 >= k):
                result_img.putpixel((i, j), 255)
            else:
                result_img.putpixel((i, j), 0)
    return result_img

def xor(img1, img2):
    width = img1.size[0]
    height = img1.size[1]
    img_result = img1.copy()
    for i in range(0, width):
        for j in range(0, height):
            pixel = abs(img2.getpixel((i, j)) - img1.getpixel((i, j)))
            img_result.putpixel((i, j), pixel)

    return img_result

image = Image.open('binarized_pict2.jpg')
#dirty_img = dirty_picture(image)
#dirty_img.save('dirty_smile.png')
rang_image = rang(image, 1)
rang_image.save('binarized_pict_1.png')
xor(image, rang_image).save('binarized_pict_1_xor.jpg')

