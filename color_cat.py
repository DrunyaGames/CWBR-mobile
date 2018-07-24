from PIL import Image
import os
import numpy as np
import colorsys


def darker_color(color):
    r, g, b = color
    h, s, v = colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)
    if v >= 0.2:
        v -= 0.2
    else:
        v = 0
    r, g, b = colorsys.hsv_to_rgb(h, s, v)
    return (r * 255, g * 255, b * 255)


def colorization(image_path, color_before, color_after):
    image_path = 'textures/items/' + image_path
    image = Image.open(image_path)
    image = image.convert('RGBA')

    data = np.array(image)
    r, g, b, a = data.T
    areas = (r == color_before[0]) & (b == color_before[1]) & (g == color_before[2]) & (a == 255)
    data[..., :-1][areas.T] = color_after
    new_image = Image.fromarray(data)
    return new_image


def color_cat(color, is_tum, is_tail, cat_id):
    im = colorization('beta_cat_texture.png', (255, 255, 255), color)
    im2 = colorization('beta_cat.png', (0, 0, 0), darker_color(color))

    im.paste(im2, (0, 0), im2)

    if is_tum:
        tum = colorization('tum.png', (0, 0, 0), darker_color(color))
        im.paste(tum, (0, 0), tum)

    if is_tail:
        tail = Image.open('textures/items/beta_cat_tail.png').convert('RGBA')
        im.paste(tail, (0, 0), tail)

    name = str(cat_id)
    path = 'temp_cats/' + name + '.png'
    im.save(path)
    return path
