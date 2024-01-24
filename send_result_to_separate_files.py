# BEGINE

import os


def line_in_annotation_file(dir, file_original):
    path = os.path.join(dir, file_original)
    name = 'res_drn_img_'

    with open(path, 'r') as file:
        lines = file.readlines()

        for i, line in enumerate(lines):
            filename = str(name) + str(i+1).zfill(2) + '.txt'
            path_res_file = os.path.join(dir, filename)

            # записываем файл аннотаций в папку базы изображений для импорта
            with open(path_res_file, 'w') as new_file:
                new_file.write(line)


# END
