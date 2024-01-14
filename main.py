# BEGINE

import os
from pathlib import Path
import cv2
import numpy
import numpy as np
from PIL import Image
import random


def view_image(image, name_of_window):
    cv2.namedWindow(name_of_window, cv2.WINDOW_AUTOSIZE)
    cv2.imshow(name_of_window, image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def write_file(data_file, data):
    data_file = open(data_file, "a+")
    data_file.write(str(data) + '\n')
    data_file.close()


def resized_image(image, percent):
    width_img, height_img = image.size
    new_width_img = int(width_img * percent)
    new_height_img = int(height_img * percent)
    new_image = image.resize((new_width_img, new_height_img))
    return new_image


def change_perspective(img):
    src_points = np.float32(
        [
            [0, 0],
            [img.shape[1] - 1, 0],
            [0, img.shape[0] - 1],
            [img.shape[1] - 1, img.shape[0] - 1],
        ]
    )

    height_percentage = random.randint(0, 20)
    reduction_pixels = int(img.shape[0] * (height_percentage / 100))

    dst_points = np.float32(
        [
            [0, 0],
            [img.shape[1] - 1, reduction_pixels],
            [0, img.shape[0] - 1],
            [img.shape[1] - 1, img.shape[0] - 1 - reduction_pixels],
        ]
    )

    M = cv2.getPerspectiveTransform(src_points, dst_points)
    perspective_view = cv2.warpPerspective(
        img, M, (img.shape[1], img.shape[0]))

    return perspective_view


def overley_image(path_bg, path_fg, file_output, scl_per_b, scl_per_t):
    background_pil = Image.open(path_bg)
    fpv_pil = Image.open(path_fg)

    scale_percent = random.randint(scl_per_b, scl_per_t) / 100
    resized_fpv = resized_image(fpv_pil, scale_percent)

    # Drone tilt angle range - "angle"
    angle = random.randint(-15, 15)
    rotate_fpv = resized_fpv.rotate(angle, expand=True)

    width_bg, height_bk = background_pil.size
    new_width_fg, new_height_fg = rotate_fpv.size

    x = random.randint(0, width_bg - new_width_fg)
    y = random.randint(0, height_bk - new_height_fg)

    start_top = x, y
    end_bottom = x + new_width_fg, y + new_height_fg

    # print(f'Box_fpv (width x height): {new_width_fg}: {new_height_fg}')

    output_coordinates = str(start_top[0]) + ' ' + str(
        start_top[1]) + ' ' + str(end_bottom[0]) + ' ' + str(end_bottom[1])

    write_file(file_output, output_coordinates)
    # print(f'Coordinates Drone (x:y)_top (x:y)_bottom : {
    #       start_top} x {end_bottom}')

    background_pil.paste(rotate_fpv,  (x, y), rotate_fpv)
    background_cv = numpy.array(background_pil)
    result_cv = cv2.cvtColor(background_cv, cv2.COLOR_BGR2RGB)

    result_cv = cv2.rectangle(result_cv, start_top,
                              end_bottom, (0, 255, 0), 2)
#
    # result_cv = change_perspective(result_cv)
#
    return result_cv


def is_image(filename):
    try:
        with Image.open(filename) as img:
            return isinstance(img, Image.Image)
    except:
        return False


# *************************************
if __name__ == '__main__':

    # Path to image in local directory
    file_res_data = 'drone coordinates.txt'

    dir_sky = 'C:/PYTHON/project-01/sky/'
    dir_fpv = 'C:/PYTHON/project-01/fpv drones/'
    dir_res = 'C:/PYTHON/project-01/result/'

    # Enter the required quantity to create "Test Images"
    str_for_iteration = 'Enter the required quantity to create "Test Images" > '
    iteration = int(input(str_for_iteration))

    # Enter the "Zoom range" for the drone: "min" & "max". Default min = 10, max = 40
    zoom_b, zoom_t = 10, 40
    # str_for_zoom = 'Enter the "Zoom range" for the Drone: "min" & "max" > '
    # zoom_b, zoom_t = map(int, input(str_for_zoom).split())

    name_file = os.path.join(dir_res, file_res_data)
    if os.path.exists(dir_res):
        my_file = open(name_file, "x")
        my_file.close()
    else:
        print("Path does not exist")

    file_list_sky = os.listdir(dir_sky)
    file_list_fpv = os.listdir(dir_fpv)

    # List of all files that are both IMG and '.png'
    images_fpv = [img for img in file_list_fpv if Path(os.path.join(
        dir_fpv, img)).suffix == '.png' and is_image(os.path.join(dir_fpv, img))]
    images_sky = [img for img in file_list_sky if Path(os.path.join(
        dir_sky, img)).suffix == '.jpg' and is_image(os.path.join(dir_sky, img))]

    # Create range(iteration) number of files with "Drone" overlay on "Sky"
    for i in range(iteration):
        name_res_jpg = 'result drone ' + str(i).zfill(2) + '.jpg'
        name_result = os.path.join(dir_res, name_res_jpg)

        num_s = int(random.randint(0, len(images_sky)))
        num_file_sky = images_sky[num_s-1]
        num_f = int(random.randint(0, len(images_fpv)))
        num_file_fpv = images_fpv[num_f-1]
        path_sky = os.path.join(dir_sky, num_file_sky)
        path_fpv = os.path.join(dir_fpv, num_file_fpv)

        result = overley_image(path_sky, path_fpv, name_file, zoom_b, zoom_t)
        cv2.imwrite(name_result, result)


# END
