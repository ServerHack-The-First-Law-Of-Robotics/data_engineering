import requests
import bs4


inn = 5262362896
url = f'https://spark-interfax.ru/search?Query={inn}'
page = requests.get(url)
html = bs4.BeautifulSoup(page.text, "html.parser")
company_link = 'https://spark-interfax.ru' + html.find('li', class_="search-result-list__item").find('a')['href']
page = requests.get(company_link)
html = bs4.BeautifulSoup(page.text, "html.parser")
tables = html.findAll('div', class_="factoids-block__item")
labels = [
    ['судебные дела', ' в качестве истца', ' в качестве ответчика'],
    ['текущие производства', 'завершенные производства'],
    ['Тендеры, количество закупок'],
    ['Существенные события за всю историю компании', 'Существенные события за текущий год'],
    ['дочерние предприятия', 'совладельцы']
]
dct = {}
for table, label in zip(tables, labels):
    cells = table.findAll('a', class_="factoid js-popup-open")
    for cell, name in zip(cells, label):
        num = cell.find('div').contents[0]
        dct[name] = int(num)
print(dct)
