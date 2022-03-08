import requests
from typing import Union

url ='http://online.igk-group.ru/ru/home?name=&ogrn=&inn='

def inn2ogrn(inn: Union[int, str]):
    r = requests.get(url + str(inn)).text[12000:]
    ind = r.index('<th>ОГРН</th>')
    return r[ind+22:ind+50].split('<')[0]

print(inn2ogrn(7842349892))