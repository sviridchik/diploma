import os

import pytesseract
from PIL import Image

os.environ.setdefault('TESSDATA_PREFIX', 'tessdata')

cures_data = ["ярина", "юритмик", "пантал", "мотилак"]
img1 = Image.open("uri.jpg")

CUSTOM_CONFIG = r" --psm 6 --oem 3 -l rus+eng"

text1 = pytesseract.image_to_string(img1, config=CUSTOM_CONFIG)
print(text1)
input_data = [el.lower() for el in text1.split()]
cures_data = [el.lower() for el in cures_data]
target = set(input_data) & set(cures_data)
if len(target) != 0:
    print('FOUND!:', target.pop())
else:
    # to do matching algo
    pass
