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
from operator import itemgetter

os.environ.setdefault('TESSDATA_PREFIX', 'tessdata')

cures_titles = [
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
    'нисит',
]
cures_titles = [el.lower() for el in cures_titles]
CUSTOM_CONFIG = r' --psm 6 --oem 3 -l rus+eng'


# def process_file(file_path):
#     print('***************', file_path)
#     img1 = Image.open(file_path)
#     text = pytesseract.image_to_string(img1, config=CUSTOM_CONFIG)
#     print(text)
#     print(process.extract(text, cures_data, scorer=fuzz.partial_ratio, limit=10))


# while True:
#     for dirpath, dirnames, filenames in os.walk('media'):
#         for file_name in filenames:
#             file_path = f'{dirpath}/{file_name}'
#             process_file(file_path)
#             os.rename(file_path, f'media_archive/{file_name}')
#     sleep(1)

# text = '''„е : ? О Г & ай
# “ „ & ВЫ й `\ [ % 2 ж\‚?/« ы ':Ы ‘«
# ШЕ [ а аГ / ва 7 ы
# я ‚ ; ‚!‚А ТР № Ч ’
# я ю 1 Й ь - д МГ 8 "і__) ‘% на Ё
# \ ' [Э ;’“. р › л *&:{. ` "З Й |
# ‚ * 4 Н щ
# ® ы т` ВЫа
# ®е 3 — ‚‘-….' РЕЧИ „Р *
# С ъ “^ ь 3 Ж_\#* р шй ? е :
# ю Р " гЭ @
# нц ы В ” х Ё У
# «а Ч - е лЕ ) ©
# — ‚ 2 е -— оЗЕНН х
# х у ЧЧ ле | |38
# ‘и рт › „й, Ч!
# ж 20 # д9° о
# ТАБЛЕТОК ра _ К
# ° ВФ — нисит оча
# 100мг СЕа лоая я
# а ) : ; 3е эа АЙЕ
# ыы 4 МитезиПае В ака сний д
# лекФарм® | льск а,
# ° Ъ‘!"‘игі
# —-
# —:_.___ь Е — 7. ь  _* - -
# М аана ннна ст оо Чена аоасьць лао ор оао оо тченраниое .'''

# text = '''
# н
# И
# С ъ
# ит
# нисит
# М аана ннна ст оо Чена аоасьць лао ор оао оо тченраниое .'''

text = """›`сп сага гоо помеа оосиницииы
в сае › ера 3
нна ес
э” .\по '`т 'пя ‘ *п-п… фнщ„ оемю!о ' /' ›_. цп‹
( ) — + рай ва у .
расе р
9 0 ‹ -— | = ‘ щ
` * » ' 1 о .
ва ро оаиа оанааеанна ннй ооаааалана я е ааааа ы аа ен да
шаы [0 к е о 7 18 то
ш (и з й х й) ъ к ) в в
8 |
ч очео аата — щ онн ‚щ‘ оооааааа онне аан нв
ь4 ' у й ё 14 5) 5)
й | @ г ет!е: ||
ул д 4 , э , : + й. »
> — е о389 воа 3
сл ё н |
› › 6 й. ю уаче 3 г епа;*{ * й — ром
шоа — нисит э®
100м!
ш— лекоарм
) 3
в оодие оыа
вааала нй ан ча ееа оа .'*'_'’"""

text = """айу йо й ° г. ай ро
ра и эй о | т ) @лу
ё ш © тэ"*›———__\ \ -й ви
- : (и в! аа — ' }
— ' эз й ) оача — :
\] к а- рои . } “ [ х в 1 ъ ' —`7" па
д : ’. ж ' г] | " ‚ \—, ч
у е — 56 е, вло [ 4 га
г > @ча о:
ь ' б ? п )_\‘ я 0 к
и 7 ( ; ю у ' ц‘ з'ё;_"` „ое
ан н ( сл вы 7
т оа ч 08
| ч зероеин 7‹‘2_1_ ы ра
ое оауа о ы
ах :"‘ н но"пе ".'‚ й л * "ё,"‚/ "
чч на кт же,
» 'ёёё%‘ : »›" ол — ай
вр ‚ р < н и с
° й# # ® ‘
е _`1у с ве 100мг
о) н о '°
й иаа е лекфарм®
оаиа в
равоелонь *{д‘ц_“*‘_ _
" 3 » ь — _ ч ю _\_—::_‘» 1‚;_" ме
: "`%‘ р ‘‹ ` ы я — ‚ а
-ч ‘ р " ы в
— ка аае м
р я, аваа " ‘ч'& ‚ %
/ & : й па ›'
‹` а 'ь‘
т й я @ а у и ':„.,‘“-"""

text = """ооа в ы   па ъёт  ёд   ъ   ж лоа   сва  лв г а м   а нь  ётё а   тд       е н  э    ё йд з      т й ф   че ёжц  оа кдяе г эна  вы   м й ойа чв ата о  ъ   ёшн   м до  ое о кана оанеь кдей е ьх  нисситт гг ы   мгя   мтеси е  в ны лекоам  чёо ы оакечн н  а о  ч   сойщ  """

print(cures_titles)
res_matches = None
for line in text.split('\n'):
    for word in line.split(' '):
        if not word:
            continue
        matches = process.extract(word.lower(), cures_titles, scorer=fuzz.ratio, limit=10)
        # print(word.lower(), matches)
        if res_matches is None:
            res_matches = matches
        else:
            matches_dict = dict(matches)
            res_matches_dict = dict(res_matches)
            res_matches = [
                (cure_title, max(res_matches_dict.get(cure_title, 0), matches_dict.get(cure_title, 0)))
                for cure_title in cures_titles
            ]

res_matches.sort(key=itemgetter(1), reverse=True)
print()
print()
print(res_matches)
