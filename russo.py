import os
from time import sleep

import pytesseract
from PIL import Image

os.environ.setdefault('TESSDATA_PREFIX', 'tessdata')

cures_data = ["ярина", "юритмик", "пантал", "мотилак"]
cures_data = [el.lower() for el in cures_data]
CUSTOM_CONFIG = r"-l rus+eng"


def process_file(file_path):
    print('***************')
    img1 = Image.open(file_path)
    text1 = pytesseract.image_to_string(img1, config=CUSTOM_CONFIG)
    print(text1)
    input_data = [el.lower() for el in text1.split()]
    target = set(input_data) & set(cures_data)
    if len(target) != 0:
        print('FOUND!:', target.pop())
    else:
        # to do matching algo
        pass


while True:
    for dirpath, dirnames, filenames in os.walk('api/media'):
        for file_name in filenames:
            file_path = f'{dirpath}/{file_name}'
            process_file(file_path)
            os.rename(file_path, f'api/media_archive/{file_name}')
    sleep(1)
