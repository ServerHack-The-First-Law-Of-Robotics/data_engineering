from parser import TenderParser
import json
import time

tender_parser = TenderParser()


def parse_category_inns_material(category: str):
    with open('material_tenders/{}_tenders.txt'.format(category)) as f:
        tenders = [i.strip() for i in f.readlines()]
    inns = {}
    mistakes = 0
    for tender_link in tenders:
        counter = 0
        if mistakes == 10:
            print('Too many problems with category')
            break
        try:
            inn = int(tender_parser.get_tender_inn(tender_link))
            if inn not in inns:
                inns[inn] = 0
            inns[inn] += 1
        except:
            time.sleep(1)
            try:
                inn = int(tender_parser.get_tender_inn(tender_link))
                if inn not in inns:
                    inns[inn] = 0
                inns[inn] += 1
            except:
                print("Couldsn't parse", tender_link)
                mistakes += 1
        counter += 1
        if counter % 100 == 0:
            print('Done {} from {}'.format(counter, len(tenders)))

    with open('material_inns/{}_inns.json'.format(category), 'w') as f:
        json.dump(inns, f)

    return inns


material2inn = {}

already_parsed = {
    'азотную кислоту (50-70 г/л) и серную кислоту (8-10 г/л)': ['20.59.52.194', '20.59.56.130'],
    'бутадиен-нитрильный каучук': ['20.17.10.141'],
    'бутадиен-стирольные и изопреновые каучуки': ['20.17.10.130', '20.17.10.120'],
    'бутадиен-стирольный каучук': ['20.17.10.130'],
    'десяти-двадцатипроцентный раствор вещества н2sо4 (серная кислота)': ['20.59.52.194'],
    'каркасная жесткая резиновая смесь': ['22.19.2'],
    'кислоту соляную (нсl) концентрированную': ['20.59.52.194'],
    'машинное масло совместно с сульфидом молибдена (формула моs2)': ['20.59.52.194', '20.14.73'],
    'мыльная эмульсия': ['20.41.31'],
    'острильная машина': ['28.41.22.140'],
    'плетеные прокладки': ['28.14.20.230'],
    'покрытие известково-солевого типа': ['20.30'],
    'аммоний молибденовокислый':[],
    'аммоний хлористый': [],
    'барабанных вулканизаторах непрерывного действия': []
    }

with open('material2tenders.json') as f:
    materials = json.load(f)

for material in materials:
    if material not in already_parsed:
        print(material)
        material2inn[material] = parse_category_inns_material(material.replace('/', ''))

with open('material2inns.json', 'w', encoding='utf-8') as f:
    json.dump(material2inn, f, ensure_ascii=False)
