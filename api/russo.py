import os
import sys
from datetime import datetime
from time import sleep

import django

sys.path.append('/home/user/work/tro/api')
os.environ['DJANGO_SETTINGS_MODULE'] = 'api.settings'
django.setup()


import pytesseract
from PIL import Image
from thefuzz import fuzz, process


os.environ.setdefault('TESSDATA_PREFIX', 'tessdata')

cures_data = [
    'ярина',
    'юритмик',
    'пантал',
    'мотилак',
    'д3 капс ультра',
    'ибупрофен',
    'арпетол',
    'вечернее',
    'омез',
    'цинк витаминс',
    'ибуфен',
]
cures_data = [el.lower() for el in cures_data]
CUSTOM_CONFIG = r' --psm 6 --oem 3 -l rus+eng'


def process_file(file_path):
    print('***************', file_path)
    img1 = Image.open(file_path)
    text = pytesseract.image_to_string(img1, config=CUSTOM_CONFIG)
    print(text)
    print(process.extract(text, cures_data, scorer=fuzz.partial_ratio, limit=10))


while True:
    for dirpath, dirnames, filenames in os.walk('media'):
        for file_name in filenames:
            file_path = f'{dirpath}/{file_name}'
            process_file(file_path)
            os.rename(file_path, f'media_archive/{file_name}')
    sleep(1)
