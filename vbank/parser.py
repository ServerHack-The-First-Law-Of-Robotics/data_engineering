import requests

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}

r = requests.get('https://vbankcenter.ru/contragent/7811533500', headers=headers).text
ind = r.index('+')
print(r[ind:ind + 20])