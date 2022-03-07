from parser import TenderParser
import json
import time

tender_parser = TenderParser()


def parse_category_inns_material(category: str):
    with open('material_tenders/{}_tenders.txt'.format(category)) as f:
        tenders = [i.strip() for i in f.readlines()]

    inns = {}
    counter = 0
    for tender_link in tenders:
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
        counter += 1
        if counter % 100 == 0:
            print('Done {} from {}'.format(counter, len(tenders)))

    with open('material_inns/{}_inns.json'.format(category), 'w') as f:
        json.dump(inns, f)


parse_category_inns_material('аммоний молибденовокислый')
