import json
from parser import TenderParser

tenders_parser = TenderParser()
with open('matset2okpdset.json') as f:
    matsetts = json.load(f)

sett2tenders = {}

for sett in matsetts:
    print(sett)
    onegood_okpd_list = matsetts[sett]
    onegood_tenders = tenders_parser.go_through_pages(onegood_okpd_list, 'onegood_tenders/{}_tenders.txt'.format(sett[:10]+'_'+sett[-10:]))
    sett2tenders[sett] = onegood_tenders
    print()

with open('sett2tenders.json', 'w', encoding='utf8') as f:
    json.dump(sett2tenders, f, ensure_ascii=False)