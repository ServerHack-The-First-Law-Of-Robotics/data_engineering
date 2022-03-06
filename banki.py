import requests
# net
# inn = '7707083893'
# bik = '046577674'

# est'
inn = '6629017176'
bik = '046577674'

url = 'https://service.nalog.ru/bi2-proc.json'
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36',
    'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7'
}
response = requests.post(url, data={
    'requestType': 'FINDPRS',
    'innPRS': inn,
    'bikPRS': bik
})

print(response.json())