import tkinter
import tkinter.font
import os


def load_font():
    guide_font = tkinter.font.Font(family="맑은 고딕", size=10, weight='bold')
    small_font = tkinter.font.Font(family="맑은 고딕", size=8, weight='bold')
    mid_font = tkinter.font.Font(family="맑은 고딕", size=14, weight='bold')
    big_font = tkinter.font.Font(family="맑은 고딕", size=18, weight='bold')
    return [guide_font, small_font, mid_font, big_font]


def load_color():
    def _from_rgb(rgb):
        return "#%02x%02x%02x" % rgb

    dark_main = _from_rgb((32, 34, 37))
    dark_sub = _from_rgb((50, 46, 52))
    dark_blue = _from_rgb((29, 30, 36))
    result_sub = _from_rgb((31, 28, 31))
    return [dark_main, dark_sub, dark_blue, result_sub]


def load_equipment_image():
    image_list = {}
    file_list = os.listdir("image")
    for i in file_list:
        if i[-3:] != 'png':
            continue
        image_list[i] = tkinter.PhotoImage(file="image/{}".format(i))
    return image_list


def load_extra_image():
    image_list = {}
    file_list = os.listdir("ext_img")
    for i in file_list:
        if i[-3:] != 'png':
            continue
        image_list[i] = tkinter.PhotoImage(file="ext_img/{}".format(i))
    return image_list


def load_weapon_image():
    image_list = {}
    file_list = os.listdir("image_wep")
    for i in file_list:
        if i[-3:] != 'png':
            continue
        image_list[i] = tkinter.PhotoImage(file="image_wep/{}".format(i))
    return image_list
