import xmltodict
import pprint
import json

with open('exported_01-05-2023.xml', 'r', encoding='utf-8') as file:
    my_xml = file.read()

my_dict = xmltodict.parse(my_xml)
my_dict = my_dict['ArrayOfProcess26DrugGrouped']
storage = []
if 'Process26DrugGrouped' in my_dict:
    # print(my_dict.keys())
    my_dict = my_dict['Process26DrugGrouped']
    for element in my_dict:
        element = element['hccdo:values']
        for el in element:
            # print(type(el))
            # print(el)
            if isinstance(el, dict):
                el = el['hccdo:drugCountryRegistrationDetails']
                if isinstance(el, dict):
                    data = el['hcsdo:drugTradeName']
                    # ['hcsdo:drugTradeName']
                    # print(data)
                    storage.append(data)

                else:
                    for e in el:
                        if isinstance(e, dict):
                            # print(e.keys())
                            # print(e['hcsdo:drugTradeName'])
                            storage.append(e['hcsdo:drugTradeName'])
                        else:
                            print(type(e))
storage = list(set(storage))
print(storage)
print(len(storage))
        # if 'hccdo:drugCountryRegistrationDetails' in el:
            # pprint.pprint(my_dict)

    # ['hccdo:values']
    # for i in range(len(my_dict)):
    #     tmp = my_dict[i]['hccdo:drugCountryRegistrationDetails']['hcsdo:drugTradeName']
    #     pprint.pprint(tmp)
storage_true = [
    'АнвиМакс',
    'В12 Анкерманн',
    'САФНЕЛО',
    'Супрастин',
    'Mucosa compositum',
    'АБАКАВИР',
    'АВВАнтацид',
    'АДЦЕТРИС',
    'АЗИТРОМИЦИН ФОРТЕ-АЛИУМ',
    'АЗИТРОМИЦИН-АЛИУМ',
    'АЛБЕНДАЗОЛ-АЛИУМ',
    'АЛЕЦЕНЗА',
    'Алзепил',
    'АЛЛЕРГОСТИН',
    'АЛЛОПУРИНОЛ АВЕКСИМА',
    'АЛПРОСТАДИЛ',
    'АЛУНБРИГ',
    'АМБРОКСОЛ',
    'АМЕЛОТЕКС',
    'АМИОДАРОН',
    'АМЛОДИПИН-ПРАНА',
    'АМОКСИЦИЛЛИН ФТ',
    'АМПРИЗИР',
    'АНАЛЬГИН',
    'АНГИОРУС',
    'Ангиорус',
    'АНТИФОЛАТ',
'АПРЕПИТАНТ',
    'АРИПЕГИС',
    'АРИФОН',
    'АРНИГЕЛЬ',
    'АРТИКАИН С ЭПИНЕФРИНОМ',
    'АСК-кардио',
    'АТОРВАСТАТИН АВЕКСИМА',
    'АТОРВАСТАТИН Фармасинтез',
    'АТОРВАСТАТИН-АЛИУМ',
    'АФЛУМЕД',
    'АЦЕКЛОФЕНАК',
    'АЦЕКЛОФЕНАК АВЕКСИМА',
    'АЦИКЛОВИР ФОРТЕ-АЛИУМ',
    'Абитера',
    'Авиамарин',
    'Агалатес',
    'Агарта',
    'Агемфил А',
    'Агтеминол',
    'Адвейт',
    'Адемпас',
    'Аденурик',
    'Адреналин',
    'Адреналин-СОЛОфарм',
    'Азалепрол',
    'Азелик',
    'Азимитем',
    'Азитромицин',
    'Азитромицин-АКОС',
    'Азурикс',
    'Аквадетрим',
    'Акимасол',
    'Аклиф',
    'Акридерм',
    'Акримекс',
    'Актовегин',
    'Алагет',
    'Алвента',
    'Алгезир Ультра',
    'Алказол',
    'Аллервэй',
    'Аллопуринол',
    'Алтея сироп-АКОС',
    'Альдуразим',
    'Альфаксим',
    'Амарил',
    'Амбизом',
    'Амбро',
    'Амбробене',
    'Амброгуд',
    'Амброксол',
    'Амброксол-Акрихин',
    'Амброксол-Фармстандарт',
    'Амивирен',
    'Амигренин',
    'Амизолид',
    'Амикацин',
    'Амиктобин',
    'Аминазин',
    'Аминокапроновая кислота-СОЛОфарм',
    'Амиодарон',
    'Амлодипин Алкалоид',
    'Амлодипин-АКОС',
    'Амлодипин-Акрихин',
    'Амлодипин-ВЕРТЕКС',
    'Амлодипин-Валсартан-Акрихин',
    'Амлодипин-КРКА',
    'Аскориксол',
'Амоксициллин + Клавулановая кислота',
    'Амоксициллин-АКОС',
    'Аморолфин',
    'Ампициллин',
    'Амприлан',
    'Амростак солофарм',
    'Амфотерицин В липосомальный',
    'Анальгин Реневал',
    'Анальгин-Ультра',
    'Анаментал',
    'Анаприлин Реневал',
    'Анастрозол',
    'Анаферон',
    'Ангидак',
    'Ангин-Хель СД',
    'Андрогель',
    'Аноро Эллипта',
    'Антиандрен',
'Антистен МВ',
    'Антифлу',
    'Апидра',
    'СолоСтар',
    'Апиксабан',
    'Апрепитант',
    'Апрепитант ПСК',
    'Апроваск',
    'Апровель',
    'Апрокан',
    'Арипипразол',
    'Арифам',
    'Аркоксиа',
    'Артезин',
    'Артерис-веро',
    'Артмелок'
,
    'Артра',
    'Артрозан',
    'Артрозилен',
    'Артрофоон',
    'Асентра',
    'Асиглия',
    'Аскорбиновая кислота',
    'Аскорил',
    'Аскорил ЛС',
    'Аскорил экспекторант',
    'Асмалиб',
    'Аспаркам Медисорб',
    'Аспирин',
    'Астмасол',
    'Атазанавир',
    'Атазанавир-КРКА',
    'Атенолол',
    'Аторвастатин',
    'Аторвастатин-АКОС',
    'Аторвастатин-ВЕРТЕКС',
    'Аторис',
    'Атровент',
    'Аттенто',
    'Аугментин',
    'Афала',
    'Афалаза',
    'Африн',
    'Ацекардол',
'Ацеклофенак',
    'Ацеклагин',
    'Ацеклофенак',
    'Ацетазоламид',
    'Ацетилсалициловая кислота',
    'Ацетилсалициловая кислота КАРДИО',
    'Ацетилсалициловая кислота Медисорб',
    'Ацетилсалициловая кислота Реневал',
    'Ацетилсалициловая кислота+Аскорбиновая кислота',
    'Ацикловир',
'Ацикловир Реневал',
'Ацикловир-АКОС',
    'Ацикловир-Акрихин',
    'Аэртал',
    'БЕНДАМУСТИН-ПРОМОМЕД',
    'БЕНЗОНАЛ',
    'БИАБЕН',
    'БИОТРАКСОН',
    'БИСОПРОЛОЛ ФТ',
    'БИСОПРОЛОЛ-ПРАНА',
    'Биспонса',
    'БОРТЕЗОМИБ-ПРОМОМЕД',
    'БРЕВИПРОСТ',
'БРЕВИПРОСТ плюс',
    'БРЕЗТРИ АЭРОСФЕРА',
    'БРИНЗОЛОЛ',
    'БРОМГЕКОМБ',
    'Бактериофаг дизентерийный поливалентный',
    'Бактофлокс',
    'Бартизар',
    'Бебифрин',
    'Бевацизумаб',
    'Беклометазон',
    'Бексеро',
    'Белара',
    'Белодерм',
    'Белосалик',
    'Бензидамин-Акрихин',
    'Бензилбензоат',
    'Бензилпенициллина натриевая соль',
    'Бензилпенициллина новокаиновая соль',
    'Бераксол-СОЛОфарм',
    'Берголак',
    'Беродуал',
    'Беротек',
    'Бетагистин',
    'Бетагистин-Акрихин',
    'Бетасерк',
    'БиКНУ',
    'Бикалутамид',
    'Билобил',
    'Бимикомби Антиглау ЭКО',
    'Бинноферон альфа',
    'Бинноферум',
    'Бипрол',
    'Бисакодил-Хемофарм',
'Бисогамма',
    'Бисопролол',
    'Бисопролол-АКОС',
    'Бисопролол-Акрихин',
    'Бисопролол-ВЕРТЕКС',
    'Бифлурин',
    'Бициллин',
'Блемарен',
    'Блеомицин-РОНЦ',
    'Блинцито',
    'БлоккоС® ХЭВИ',
    'Боботик',
    'Бозенекс',
    'Бозентан',
    'Бонспри',
    'Боргитол',
    'Борная кислота Реневал',
    'Бортезол',
    'Бортезомиб-Тева',
    'Боярышника настойка Реневал',
    'Бравадин',
    'Брайдан',
    'Брафтови',
    'Бретарис® Дженуэйр®',
    'Бриллиантовый зеленый',
    'Брим Антиглау ЭКО',
    'Бримайза® Дуо',
    'Бримонидин-СЗ',
    'Бромгексин',
    'Бромгексин Медисорб',
    'Бромокриптин',
    'Бромфенак-СЗ',
    'Бронхалис-Хель',
    'Бронхипрет',
    'Бронхорус',
    'Бумидол',
    'Бутадион',
    'Бутамират-Фармстандарт',
    'Быструм Спринт',
    'ВАКТРИВИР Комбинированная вакцина против кори, краснухи и паротита культуральная живая',
    'ВАЛГАНОЛЕК',
    'ВАЛИДОЛ С ИЗОМАЛЬТОМ',
'ВАЛСАРТАН',
    'ВАЛСАРТАН-АЛИУМ',
    'ВЕНАРУС',
    'ВЕНДИОЛ',
    'ВИЗАННА',
    'ВИАЛАВ',
    'ВИЗОККО',
    'ВИЛДАГЛИПТИН',
    'ВИНПОЦЕТИН',
    'ВИНПОЦЕТИН-АЛИУМ',
    'Вабисмо',
    'Вазелин Реневал',
    'Вазенекс',
    'Вазилип',
    'ВаксигрипТетра',
    'Валацикловир',
    'Валацикловир-АКОС',
    'Валацикловир-Тева',
    'Валганцикловир',
    'Валеотиниб',
    'Валериана Форте',
    'Валерианахель',
    'Валерианы настойка Реневал',
    'Валерианы экстракт',
    'Валидол',
    'Валраксет',
    'Валсартан-Акрихин',
    'Вальдоксан',
    'Вальсакор',
    'Вальсакор',
    'Ванкорус',
    'Варгатеф',
    'Варденафил-КРКА',
    'Варивакс',
    'Вартоцид',
    'Варфарин',
    'Велаксин',
    'Вельтасса',
    'Венарус',
    'Венолайф',
    'Венолайф Дуо',
    'Верапамил',
    'Верзенио',
    'Веркуво',
    'Веро-амлодипин',
    'Веро-винкристин',
    'Веротрексед',
    'Верошпилактон',
    'Верошпилактон',
    'Вертигохель',
    'Вескомид',
    'Виагра',
    'Вибуркол',
    'Визарсин',
    'Вилдаглиптин Медисорб',
    'Вилдаглиптин-СЗ',
    'Вилдус',
    'Вимизайм',
    'Виндакель',
    'Винпоцетин форте',
    'Винпоцетин-OBL',
    'Винпоцетин-АКОС',
    'Вирфотен',
    'Висмута трикалия дицитрат',
    'Витамин D3',
    'Витапрост',
    'Вифенд',
    'Вода для инъекций',
    'Вокабриа',
'Вольтарен',
    'Вольтарен',
    'Вольтарен Эмульгель',
    'Воцинти',
    'ГЕВИРАН',
    'ГЕМТРАНИКС',
    'ГЕМЦИТАБИН-ПРОМОМЕД',
    'ГЕСПЕРИДИН+ДИОСМИН',
    'ГЕТИНЕКС',
    'ГЕФИТИНИБ-ТЛ',
    'ГИНКОУМ',
    'ГИПОСАРТ',
    'Габапентин',
    'Гадобускан',
    'Гадопетоскан',
    'Газива',
    'Газилак',
    'Галазолин',
    'Галантамин',
    'Галвус Мет',
    'Галвус',
    'Галидор',
    'Галиум-хель',
    'Гальнора',
    'Ганатон',
    'Гасит',
    'Гастал',
    'Гастрикумель',
    'Гастрозол',
    'Гастростат',
    'Гаттарт',
    'Гексикон',
    'Гексимистин',
    'Гексэтидин',
    'Гексэтидин-Акрихин',
    'Гельминдазол',
    'Гемангиол',
    'Гемлибра',
    'Гемцивин',
    'Гемцитабин-РОНЦ',
    'Гемцитабин-Тева',
    'Генферон',
    'Гепабене',
    'Гепар композитум',
    'Гепарин',
    'Гепарин-Акрихин',
    'Гептрал',
    'Гербион',
    'Гефтесса',
    'Гидазепам',
    'Гидрасек',
    'Гидрокортизон-АКОС',
    'Гидрокортизон-АКОС',
    'Гидроксиэтилкрахмал',
    'Гидрохлоротиазид + Лозартан',
    'Гидрохлоротиазид+Каптоприл',
    'Гинекохель',
    'Гинофорт',
'Гиотриф',
    'Гипосарт А',
    'Гипосарт Н',
    'Гипотиазид',
    'Гирель',
    'Глибенфаж',
    'Глидиаб МВ',
    'Гликлада',
    'Гликлазид МВ',
    'Гликлазид-СЗ',
    'Гликсамби',
    'Глимепирид',
    'Глипвило',
    'Глицерин',
    'Глицерин Реневал',
    'Глюкоза',
    'Глюренорм',
    'Голда МВ',
    'Гормель СН',
    'Грамисепт',
    'Грандаксин',
    'Гранисетрон',
    'Гриптера',
    'Гроприносин',
    'Д-пантенол-Нижфарм',
    'Д3-КАПС МАКСИМА',
    'Д3-КАПС УЛТРА',
    'ДАБИГАТРАН',
    'ДАРУНАВИР-НАНОЛЕК',
    'ДЕ-ВИСМУТ',
    'ДЕКСОНАЛ',
    'Детралекс',
    'ДЕТРАЛЕКС',
    'ДЕТРАПРОКТ',
    'Детромбин',
    'ДЕФАСТЭРА',
    'ДЕФЕРАЗИРОКС-ХИМРАР',
    'Джосет',
    'ДОБРОКАМ',
    'ДОПЕГИТ',
    'ДРОПЕРИДОЛ',
    'Дабиксом',
    'Дайвобет',
    'Даларгин-Эллара',
    'Далацин',
    'Дальнева',
    'Дальтеп',
    'Дантриум',
    'Дапафорс',
    'Дарбинес',
    'Дарунавир',
    'Даунорубицин-ЛЭНС',
    'Девирс',
    'Девирс',
    'Дезлоратадин-АКОС',
    'Дезринит',
    'Дексалгин',
    'Дексаметазон',
    'Дексаметазон-КРКА',
    'Дексиакс',
    'Дексилант',
    'Декскетопрофен',
    'Декскетопрофен-СЗ',
    'Декспантенол Реневал',
    'Декспантенол-ВЕРТЕКС',
    'Дельтиба',
    'Депакин',
    'Дермовейт',
    'Детравенол',
    'Детралекс',
    'Деферазирокс',
    'Децитана',
    'Джадену',
    'Джевтана',
    'Джент',
    'Джулука',
    'Диабеталонг',
    'Диабетон',
    'Диазоксид',
    'Диазолин',
    'Диакарб',
    'Диалрапид',
    'Диапаглиф',
    'Диара',
    'Диартрин',
    'Диафурил',
    'Дибикор',
    'Диваза',
    'Дигоксин Реневал',
    'Дизаверокс',
    'Дикардплюс',
    'Диклофенак',
    'Дилтиазем',
    'Диметинден-Акрихин',
    'Динамико',
    'Динобутин',
    'Диовенгес',
    'Диоксидин',
    'Дипана',
    'Дипиридамол',
    'Дипиридамол-ФПО',
'Дипроспан',
    'Дискус композитум',
    'Диспевикт',
    'Дифлюкан',
    'Довато',
    'Доквир',
    'Доксазозин-ФПО',
    'Доксиламин',
    'Доксициклин Солюшн Таблетс',
    'Доксициклин ЭКСПРЕСС',
    'Долобене',
    'Домперидон-Тева',
    'Донормил',
    'Допацептин',
    'Дор Антиглау ЭКО',
    'Дорзиал плюс',
    'Дорзоламид-СЗ',
    'Дорзолан',
    'Дорипенем',
    'Дортимол Антиглау ЭКО',
    'Дофамин',
    'Дриптан',
    'Дротаверин Реневал',
    'Дротаверин-СОЛОфарм',
    'Дулоксента',
    'Дуодарт',
    'Дуоденохель',
    'Дутастерид Фармасинтез',
    'Дутастерид-Тева',
    'ДэТриФерол',
    'Дюспаталин',
    'Дюфастон',
    'Ервой',
    'ЖЕЛЕЗА (III) ГИДРОКСИД САХАРОЗНЫЙ КОМПЛЕКС',
    'Жавлор',
    'Железа [III] гидроксид сахарозный комплекс',
    'ЗАФРИЛЛА',
    'ЗИДОВУДИН+ЛАМИВУДИН',
    'ЗОВАРТ',
    'ЗОВИРАКС',
    'ЗОПИКЛОН ФТ',
    'Залаин',
    'Заласта',
    'Залтрап',
    'Звездочка ноз',
    'Зелбораф',
    'Зеникс',
    'Зербакса',
    'Зидовудин',
    'Зидолам',
    'Зилт',
    'Золакса ОДТ',
    'Золгенсма',
'Золера',
    'Зульбекс',
    'ИБУПРОФЕН',
    'ИВЛИЗИ',
    'ИМАТИНИБ ГРИНДЕКС'
    'ИММУНОЗИН',
    'ИМОВАКС ПОЛИО',
    'ИНОПРАЗИН',
    'ИНСПИРАКС',
    'ИПИДАКРИН',
    'ИПИКРАТ',
    'ИРБЕСАРТАН',
    'ИРИНОТЕКАН-БЕЛМЕД',
    'ИРИНОТЕКАН-ПРОМОМЕД',
    'Ибандроновая кислота',
    'Ибупрофен',
    'Ибупрофен -АКОС',
    'Ибупрофен Медисорб',
    'Ивабрадин',
    'Ивилект',
    'Ивинак',
    'Иглинид',
    'Изопринозин',
    'Изосорбида мононитрат',
    'Изофра',
    'Икатибант солофарм',
    'Икатибант-Тева',
    'Икервис',
    'Иловерум',
    'Илпио',
    'Иматанго',
    'Иматиниб-Тева',
    'Иммунат',
    'Иммунин',
    'Импаза',
    'Импликор',
    'Имунофан',
    'Индапамид',
    'Индигокармин',
    'Индовазин',
    'Индоксил',
    'Индометацин ',
    'Инкресинк',
    'Инлита',
    'Иновелон',
    'Инспиракс',
    'Инстолит',
    'Интегрилин',
    'Инфира',
    'Ионоплазм',
    'Ипидакрин-АЛИУМ',
    'Ипидакрин-СЗ',
    'Ипратерол',
    'Ипратропиум',
    'Иринова',
    'Ириноплат',
    'Иритен',
    'Итомед',
    'Итоприд',
    'Итулси',
    'Ихтиол Реневал',
    'Йогексол-АКОС',
    'Йод',
    'Йодбаланс',
    'Йопроскан',
    'КАБАЗИТАКСЕЛ-ПРОМОМЕД',
    'КАБАЗИТАКСЕЛ-ФР',
    'КАВИНТОН',
    'КАРБАМАЗЕПИН ФАРМЛЭНД',
    'Кетилепт',
    'КЕТОРОЛАК',
    'КЕТОРОЛАК ВЕЛФАРМ',
    'КЛАРИТРОМИЦИН',
    'КЛОЗАПИН АВЕКСИМА',
    'КОВИД-глобулин',
    'КОРАКСАН',
    'Кордарон',
    'КОРДАРОН',
    'КОФЕИН-БЕНЗОАТ НАТРИЯ',
    'КСИЛИН',
    'КСОНОКТАМ',
    'КСОФЛЮЗА',
    'Каберголин',
    'Кавинтон',
    'Кадсила',
    'Календулы настойка Реневал',
    'Калетра',
    'Калидавир',
    'Калия и магния аспарагинат',
    'Калия оротат',
    'Калия хлорид',
    'Калькохель',
'Кальцемара',
    'Кальций Д3',
    'Кальция глюконат',
    'КамРОУ',
    'Камирен'







]