import requests
import bs4

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}

r = requests.get("https://utp.sberbank-ast.ru/Trade/NBT/PurchaseView/21/0/0/790170", headers=headers)
print(bs4.BeautifulSoup(r.text).prettify())

144082846
