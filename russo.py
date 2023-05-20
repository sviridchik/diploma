import os
from time import sleep

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
    def remove_short_matches(matches: list, initial: str):
        return [match for match in matches if len(match[0]) >= len(initial)]

    print('***************', file_path)
    img1 = Image.open(file_path)
    text = pytesseract.image_to_string(img1, config=CUSTOM_CONFIG)
    print(text)
    print(process.extract(text, cures_data, scorer=fuzz.partial_ratio, limit=10))
    best_match_by_med = list()
    for med in cures_data:
        matches = process.extract(med, text.split('\n'), scorer=fuzz.partial_ratio, limit=10)
        matches = remove_short_matches(matches, med)
        # print(med, matches)
        if len(matches) == 0:
            top_match_score = 0
        else:
            top_match_score = matches[0][1]

        best_match_by_med.append((top_match_score, med))

    print(sorted(best_match_by_med, reverse=True))


while True:
    for dirpath, dirnames, filenames in os.walk('api/media'):
        for file_name in filenames:
            file_path = f'{dirpath}/{file_name}'
            process_file(file_path)
            os.rename(file_path, f'api/media_archive/{file_name}')
    sleep(1)

# text = '''}
# ш
# у у
# й,
# и :
# КЕ оаЛ '
# ——спцЕнит” ' й
# аао оожоя ы к ж кцу о т ВА бр о НО
# @ - сооЗвщкОвСКИЙ завод медищинск “4@
# ’ К пча сурая аКОар ВаОВРОССНя
# } ОН Ю Р ) С е
# оо таоле н_&ко К @ ;‹ р кр ех
# аее 7 пленочи — оболос ИЫг ^
# еаьО. оОО а, Гр е ИСКРМГ й
# : оана ао олН аОСВ =
# ке ЗЫТОЕ ЗКа ЛЫЕОе Обиество
# ` ° р ыс '-‘ ‘Э ЕИхреп#ратов* м
# ья ‹ @ уа Ис , ИХ
# В .Ъ‚‚ р ГЪ .] ; # }
# Й а _\‚›!,д@ я т ‘_0‚:' .
# л ао ‚'\А—'\_\д*‹ А ь,‚:ъ‘._ъ}__;_ « лЧС у
# ЧОУОБТОК НОКоке ТЫх пленочно' КОЙ о 200 »
# В!
# В :
# Ва
# о
# ,
# ЫЕ ' &
# ы Ц 'а.› оы'''

# med = 'пленочная'
# print(text.split('\n'))
# print(fuzz.ratio(med, text))  # NO
# print(fuzz.partial_ratio(med, text))
# print(fuzz.token_set_ratio(med, text))  # NO
# print(fuzz.partial_token_set_ratio(med, text))  # likely no
# print(process.extract(text, cures_data, scorer=fuzz.partial_ratio, limit=10))