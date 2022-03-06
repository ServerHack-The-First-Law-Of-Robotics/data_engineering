import requests
import bs4

inn = 7726402390
url = f'https://e-ecolog.ru/entity/{inn}/finance'
page = requests.get(url)
html = bs4.BeautifulSoup(page.text, "html.parser")
years = html.findAll('div', class_='mb-20 border-t border-gray-200')
dct = {}
for y in years:
    year_num = y.find('a')['name']
    dct[year_num] = {}
    table = y.find('div', class_='grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-2')
    for cell in table.findAll('div'):
        title = cell.find('b').contents[0]
        if cell.find('span') is not None:
            value = cell.find('span').contents[0].replace('\u2009', '')
            if '₽' in value:
                value = value.replace('₽', '')
                if 'млн' in value:
                    value = float(value.replace('млн', '').replace(',', '.').replace('−', '-')) * (10 ** 6)
                elif 'тыс' in value:
                    value = float(value.replace('тыс', '').replace(',', '.').replace('−', '-')) * (10 ** 3)
                elif 'млрд' in value:
                    value = float(value.replace('млрд', '').replace(',', '.').replace('−', '-')) * (10 ** 9)
        else:
            value = None
        dct[year_num][title] = value

print(dct)
