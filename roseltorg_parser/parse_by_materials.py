from m2o import material2okpd
from parser import TenderParser
import json

tenders_parser = TenderParser()

material2tenders = {}

for material in material2okpd:
    print(material)
    material_okpd_list = material2okpd[material]
    onegood_tenders = tenders_parser.go_through_pages(material_okpd_list, 'material_tenders/{}_tenders.txt'.format(material))
    material2tenders[material] = onegood_tenders
    print()

with open('material2tenders.json', 'w', encoding='utf8') as f:
    json.dump(material2tenders, f, ensure_ascii=False)