import requests


inn = 7707083893
t = requests.post('https://egrul.nalog.ru/', data={'query': inn}).json()['t']
t2 = requests.get(f'https://egrul.nalog.ru/search-result/{t}').json()
t3 = t2['rows'][0]['t']
requests.get(f'https://egrul.nalog.ru/vyp-request/{t3}')
requests.get(f'https://egrul.nalog.ru/vyp-status/{t3}')
d = requests.get(f'https://egrul.nalog.ru/vyp-download/{t3}', stream=True)

d.raise_for_status()

with open('../123.pdf', 'wb') as handle:
    for block in d.iter_content(1024):
        handle.write(block)
