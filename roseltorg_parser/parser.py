import requests
from typing import List
from bs4 import BeautifulSoup


class TenderParser():
    def __init__(self):
        pass

    def get_tenders(self, okpds: List[str], statuses: List[int] = [0, 1, 2, 3, 4], sale: int = 1, currency: str = 'all',
                    source: int = 7, page = 0):
        payload = [('okpd2%5B%5D', okpd) for okpd in okpds] + \
                  [('sale', sale),
                   ('currency', currency),
                   ('source%5B%5D', source)] + \
                  [('status%5B%5D', status) for status in statuses]
        if page:
            payload.append(('page', page))
            payload.append(('from', page * 10))
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}
        r = requests.get('https://www.roseltorg.ru/procedures/search', params=payload, headers=headers)
        pages = BeautifulSoup(r.text, 'html.parser').find_all('a', class_='search-results__link')
        hrefs = [page['href'] for page in pages]
        return hrefs

    def go_through_pages(self, okpds: List[str], dumpfile_name: str):
        all_hrefs = []
        page_num = 0
        while True:
            try:
                hrefs = self.get_tenders(okpds, page = page_num)
                all_hrefs += hrefs
                with open(dumpfile_name, 'a') as f:
                    for href in hrefs:
                        f.write(href + '\n')
                page_num += 1
            except:
                print(page_num)
                break
        return all_hrefs


    def get_buyers(self, okpd: str):
        tenders = self.get_tenders([okpd])

    def get_tender_inn(self, tender_link: str):
        return self.get_tender_page(tender_link).find_all('p', class_='data-table__info')[1].contents[0].split('ИНН')[-1][:-1]

    def get_tender_page(self, tender_link: str):
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}
        r = requests.get('https://www.roseltorg.ru' + tender_link, headers=headers)
        # print('got it')
        # print(r.request.url)
        return BeautifulSoup(r.text, 'html.parser')

    def get_tender_doc(self, tender_link: str):
        soup = self.get_tender_page(tender_link)
        # print(soup)
        search = soup.find_all('a', title='Протокол рассмотрения вторых частей заявок')
        if search:
            for doc in search:
                print(doc)
                if 'file-rtf' in doc['class']:
                    print(doc['href'])
        search = soup.find_all('a', title='Протокол рассмотрения заявок')
        if search:
            for doc in search:
                if 'file-rtf' in doc['class']:
                    print(doc['href'])




# print(TenderParser().get_tender_inn('/procedure/0372100029922000109'))


