
from PIL import Image, ImageFont, ImageDraw
from fontTools.ttLib import TTFont
from math import ceil
from Otsu_binarization import Otsu_binarization
import numpy as np

font = TTFont("fonts/KZ_Times.ttf")
cmap = font['cmap']
t = cmap.getcmap(3, 1).cmap
s = font.getGlyphSet()
units_per_em = font['head'].unitsPerEm


def get_text_width(text, point_size):
    total = 0
    for c in text:
        if ord(c) in t and t[ord(c)] in s:
            total += s[t[ord(c)]].width
        else:
            total += s['.notdef'].width
    total = total * float(point_size) / units_per_em
    return total


KZ_LETTERS = [
    'А', 'Ә', 'Б', 'В', 'Г', 'Ғ', 'Д', 'Е', 'Ё',
    'Ж', 'З', 'И', 'Й', 'К', 'Қ', 'Л', 'М', 'Н',
    'Ң', 'О', 'Ө', 'П', 'Р', 'С', 'Т', 'У', 'Ұ',
    'Ү', 'Ф', 'Х', 'Һ', 'Ц', 'Ч', 'Ш', 'Щ', 'Ъ',
    'Ы', 'І', 'Ь', 'Э', 'Ю', 'Я'
]

font = ImageFont.truetype("fonts/KZ_Times.ttf", 52)

for i, letter in enumerate(KZ_LETTERS):
    width = get_text_width(letter, 52)

    img = Image.new(mode="RGB", size=(ceil(width), 52), color="white")

    draw = ImageDraw.Draw(img)

    draw.text((0, 0), letter, (0, 0, 0), font=font)

    Image.fromarray(Otsu_binarization(np.array(img)), 'L').save(f"казахские черные/{i + 1}.png")