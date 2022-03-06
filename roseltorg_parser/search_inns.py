from parser import TenderParser
import json
import time

tender_parser = TenderParser()


def parse_category_inns(category: str):
    with open('{}_tenders.txt'.format(category)) as f:
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
            time.sleep(5)
            try:
                inn = int(tender_parser.get_tender_inn(tender_link))
                if inn not in inns:
                    inns[inn] = 0
                inns[inn] += 1
            except:
                print("Couldsn't parse", tender_link)
        counter += 1
        if counter % 1000 == 0:
            print('Done {} from {}'.format(counter, len(tenders)))

    with open('{}_inns.txt'.format(category), 'a') as f:
        for inn in inns:
            f.write(str(inn) + '\n')

    with open('{}_inns.json'.format(category), 'w') as f:
        json.dump(inns, f)


parse_category_inns('metal')
