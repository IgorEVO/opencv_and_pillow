# BEGINE

import os
import random
import shutil
from pathlib import Path


def files_to_dataset(dir_res, path_Dataset):
    path_test_img = Path(path_Dataset, 'test/images')
    path_test_txt = Path(path_Dataset, 'test/labels')
    path_train_img = Path(path_Dataset, 'train/images')
    path_train_txt = Path(path_Dataset, 'train/labels')
    path_valid_img = Path(path_Dataset, 'valid/images')
    path_valid_txt = Path(path_Dataset, 'valid/labels')

    # We get a list of files in the "result" directory and mix the list of files randomly
    all_list_jpg = [file for file in Path(
        dir_res).iterdir() if file.suffix == '.jpg']

    random.shuffle(all_list_jpg)

    # We calculate the number of files for each list in the ratio 7:2:1
    train_count = int(len(all_list_jpg) * 0.7)
    valid_count = int(len(all_list_jpg) * 0.2)
    test_count = len(all_list_jpg) - train_count - valid_count

    # Create lists for each part
    train = all_list_jpg[:train_count]
    valid = all_list_jpg[train_count:train_count+valid_count]
    test = all_list_jpg[train_count+valid_count:]

    # Moving files to new directories
    for file in train:
        shutil.move(file, os.path.join(path_train_img, file.name))
        txt_name = file.with_suffix(".txt")
        shutil.move(txt_name, os.path.join(path_train_txt, txt_name.name))

    for file in valid:
        shutil.move(file, os.path.join(path_valid_img, file.name))
        txt_name = file.with_suffix(".txt")
        shutil.move(txt_name, os.path.join(path_valid_txt, txt_name.name))

    for file in test:
        shutil.move(file, os.path.join(path_test_img, file.name))
        txt_name = file.with_suffix(".txt")
        shutil.move(txt_name, os.path.join(path_test_txt, txt_name.name))

    print(f'\nAll files have been moved to folders: test/train/valid')

# END
