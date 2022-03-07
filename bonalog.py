import requests


inn = 7726402390
company_info = requests.get(f'https://bo.nalog.ru/nbo/organizations/search?query={inn}&page=0')
