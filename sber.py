import requests
import re
import bs4

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36',
    'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7'
}
# url = 'https://utp.sberbank-ast.ru/Trade/SearchQuery/PurchaseList'
# xml =\
#     """
# <elasticrequest><filters><mainSearchBar><value></value><type>best_fields</type><minimum_should_match>100%</minimum_should_match></mainSearchBar><purchAmount><minvalue></minvalue><maxvalue></maxvalue></purchAmount><PublicDate><minvalue></minvalue><maxvalue></maxvalue></PublicDate><PurchaseStageTerm><value></value><visiblepart></visiblepart></PurchaseStageTerm><CustomerCondition><value></value></CustomerCondition><CustomerDictionary><value></value></CustomerDictionary><customer><visiblepart></visiblepart></customer><RegionNameTerm><value></value><visiblepart></visiblepart></RegionNameTerm><RequestStartDate><minvalue></minvalue><maxvalue></maxvalue></RequestStartDate><RequestDate><minvalue></minvalue><maxvalue>01.02.2022 00:00</maxvalue></RequestDate><AuctionBeginDate><minvalue></minvalue><maxvalue></maxvalue></AuctionBeginDate><okdp2MultiMatch><value></value></okdp2MultiMatch><okdp2tree><value>"0_306_164576", "0_306_163167"</value><productField>productId</productField><branchField>BranchFullId</branchField></okdp2tree><classifier><visiblepart>22: Изделия резиновые и пластмассовые, 25: Изделия...</visiblepart></classifier><orgCondition><value></value></orgCondition><orgDictionary><value></value></orgDictionary><organizator><visiblepart></visiblepart></organizator><PurchaseWayTerm><value></value><visiblepart></visiblepart></PurchaseWayTerm><BranchNameTerm><value></value><visiblepart></visiblepart></BranchNameTerm><IsSMPTerm><value></value><visiblepart></visiblepart></IsSMPTerm><purchCurrency><value></value><visiblepart></visiblepart></purchCurrency><statistic><totalProc>393</totalProc><TotalSum>1.63 Млрд.</TotalSum><DistinctOrgs>132</DistinctOrgs></statistic></filters><fields><field>TradeSectionId</field><field>purchAmount</field><field>purchCurrency</field><field>purchCodeTerm</field><field>purchCode</field><field>PurchaseTypeName</field><field>purchStateName</field><field>OrgName</field><field>SourceTerm</field><field>PublicDate</field><field>RequestDate</field><field>RequestStartDate</field><field>RequestAcceptDate</field><field>AuctionBeginDate</field><field>auctResultDate</field><field>CreateRequestHrefTerm</field><field>CreateRequestAlowed</field><field>purchName</field><field>SourceHrefTerm</field><field>objectHrefTerm</field><field>needPayment</field><field>IsSMP</field><field>isIncrease</field><field>IntegratorCode</field><field>IntegratorCodeTerm</field><field>PurchaseExplanationRequestHrefTerm</field><field>PurchaseId</field><field>PurchaseTypeType</field><field>ESG</field></fields><sort><value>default</value><direction></direction></sort><aggregations><empty><filterType>filter_aggregation</filterType><field></field><min_doc_count>0</min_doc_count><order>asc</order></empty></aggregations><size>20</size><from>0</from></elasticrequest>    """
# data = {'xmlData': xml}
# page = requests.post(url, data=data, headers=headers)
# xml = page.json()['data']['Data']['tableXml']
# links = [m.group() for m in re.finditer(r'https://utp.sberbank-ast.ru/Trade/NBT/PurchaseView/\d+/\d+/\d+/\d+', xml)]
# print(links)
# print(len(links))

url = 'https://utp.sberbank-ast.ru/Trade/NBT/PurchaseView/21/0/0/790170'
page = requests.get(url, headers=headers)
html = bs4.BeautifulSoup(page.text, "html.parser")
table = html.find('table', {'id': 'Protocols_ProtocolInfoRO', 'name': 'Protocols_ProtocolInfo', 'table-type': "htable"}).find('tbody')
last_row = table.findAll('tr')[-3]
# needed = last_row.findChildren('td', recursive=True)[1]
print(last_row)
# print(needed.find('a'))
# print(len(table.findAll('tr', recursive=True)))
