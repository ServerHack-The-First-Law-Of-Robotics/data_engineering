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

with open('material2tenders.json') as f:
    materials = json.load(f)

for material in materials:
    print(material)
    material2inn[material] = parse_category_inns_material(material.replace('/', ''))

with open('material2inns.json', 'w', encoding='utf-8') as f:
    json.dump(material2inn, f, ensure_ascii=False)
