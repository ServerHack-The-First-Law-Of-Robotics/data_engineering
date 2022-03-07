import requests
from typing import List
from bs4 import BeautifulSoup


class TenderParser():
    def __init__(self):
        pass

    def get_tenders(self, okpds: List[str], page_num=0):
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}
        url = 'https://www.roseltorg.ru/procedures/search?sale=1&status%5B%5D=0&status%5B%5D=1&status%5B%5D=2&status%5B%5D=3&status%5B%5D=4&'
        for okpd in okpds:
            url += 'okpd2%5B%5D=' + okpd + '&'
        url += 'currency=all'
        if page_num:
            url += '&page=' + str(page_num) + '&from=' + str(page_num * 10)
        r = requests.get(url, headers=headers)
        # print(r.request.url)
        pages = BeautifulSoup(r.text, 'html.parser').find_all('a', class_='search-results__link')
        hrefs = [page['href'] for page in pages][::2]
        return hrefs

    def go_through_pages(self, okpds: List[str], dumpfile_name: str):
        all_hrefs = []
        dumpfile_name = dumpfile_name.replace('/', '')
        page_num = 0
        while page_num < 50:
            try:
                hrefs = self.get_tenders(okpds, page_num=page_num)
                all_hrefs += hrefs
                with open(dumpfile_name, 'a') as f:
                    for href in hrefs:
                        f.write(href + '\n')
                page_num += 1
            except:
                break
        print(page_num)

        return all_hrefs

    def get_buyers(self, okpd: str):
        tenders = self.get_tenders([okpd])

    def get_tender_inn(self, tender_link: str):
        txt = self.get_tender_page(tender_link)
        ind_inn = txt.index('(ИНН ')
        return txt[ind_inn + 5: ind_inn + 15]

    def get_tender_page(self, tender_link: str):
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}
        r = requests.get('https://www.roseltorg.ru' + tender_link, headers=headers)
        # print('got it')
        # print(r.request.url)
        return r.text

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
