from PIL import Image, ImageDraw
import numpy as np


def semitone(old_image):
    return (0.3 * old_image[:, :, 0] + 0.59 * old_image[:, :, 1] + 0.11 * old_image[:, :, 2]).astype(np.uint8)

