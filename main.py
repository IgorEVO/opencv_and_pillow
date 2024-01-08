# BEGINE

import os
import cv2
import numpy
from PIL import Image
import random


def viewImage(image, name_of_window):
    cv2.namedWindow(name_of_window, cv2.WINDOW_AUTOSIZE)
    cv2.imshow(name_of_window, image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def writeFile(data_file, data):
    data_file = open(data_file, "a+")
    data_file.write(str(data) + '\n')
    data_file.close()


def overleyImage(path_bg, path_fg, file_output):
    background_pil = Image.open(path_bg)
    fpv_pil = Image.open(path_fg)

    try:
        background_pil = Image.open(path_sky)
    except FileNotFoundError:
        print('File "Sky HD.jpg" not found')
    try:
        fpv_pil = Image.open(path_fpv)
    except FileNotFoundError:
        print('File "dron_ok.png" not found')

    width_bg, height_bk = background_pil.size
    width_fg, height_fg = fpv_pil.size

    scale_percent = random.randint(10, 50) / 100
    new_width_fpv_pil = int(width_fg * scale_percent)
    new_height_fpv_pil = int(height_fg * scale_percent)

    new_image = fpv_pil.resize((new_width_fpv_pil, new_height_fpv_pil))

    x = random.randint(0, width_bg - new_width_fpv_pil)
    y = random.randint(0, height_bk - new_height_fpv_pil)
    coordinates = x, y

    writeFile(file_output, coordinates)
    print(f'x:y = {x} : {y}')

    background_pil.paste(new_image,  (x, y), new_image)
    background_cv = numpy.array(background_pil)
    result = cv2.cvtColor(background_cv, cv2.COLOR_BGR2RGB)
    return result


# Path to image in local directory
dir_sky = 'C:/PYTHON/project_01/sky/'
file_sky = 'Sky HD.jpg'
path_sky = os.path.join(dir_sky, file_sky)

dir_fpv = 'C:/PYTHON/project_01/fpv/'
file_fpv = 'dron_ok.png'
path_fpv = os.path.join(dir_fpv, file_fpv)

dir_res = 'C:/PYTHON/project_01/result/'
file_res = 'drone coordinates.txt'

if os.path.exists(dir_res):
    name_file = os.path.join(dir_res, file_res)
    my_file = open(name_file, "x")
    my_file.close()
else:
    print("Path does not exist")

for i in range(15):
    name_res_jpg = 'result drone ' + str(i).zfill(2) + '.jpg'
    name_result = os.path.join(dir_res, name_res_jpg)
    result = overleyImage(path_sky, path_fpv, name_file)

    cv2.imwrite(name_result, result)


# END
