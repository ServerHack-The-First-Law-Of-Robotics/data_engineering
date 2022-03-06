import requests
import bs4
import json
from tqdm import tqdm

user_agent = 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; de-at) AppleWebKit/533.21.1 (KHTML, like Gecko) Version/5.0.5 Safari/533.21.1'
headers = {'User-Agent': user_agent}
base_url = 'https://www.rusprofile.ru/codes/220000'
dct = {}
last = requests.get(base_url, headers=headers)
for n in tqdm(range(2, 353)):
    url = base_url + f'/{n}'
    try:
        page = requests.get(url, headers=headers)
        html = bs4.BeautifulSoup(page.text, "html.parser")
        companies = html.findAll('div', class_='company-item')
        for comp in companies:
            status = comp.find('div', class_='company-item-status')
            if status is not None:
                continue

            name = comp.find('div', class_='company-item__title').find('a').contents[0].strip()
            info = comp.findAll('div', class_='company-item-info')[1].findAll('dl')
            inn = info[0].find('dd').contents[0].strip()
            ogrn = info[1].find('dd').contents[0].strip()

            dct[name] = {'inn': inn, 'ogrn': ogrn}
        print(page == last)
        with open('../data2.json', 'w') as fp:
            json.dump(dct, fp)

    except Exception as e:
        print(e)
        with open('../error.html', 'w') as file:
            file.write(page.text)

with open('../data2.json', 'w') as fp:
    json.dump(dct, fp)

print(dct)
print(len(dct))

