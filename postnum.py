import requests
import re

from bs4 import BeautifulSoup

srchwrd = '광덕 2로'
url = 'http://openapi.epost.go.kr/postal/retrieveNewAdressAreaCdService/retrieveNewAdressAreaCdService/getNewAddressListAreaCd'
params = {
    'serviceKey': '7kEsxVN9P4SCOTTBAmWPvKJQDrhW4i08XbJe98mkPpthjKeB6bQjiDMSEJuNHVroSg3sx8OUYLaeSIe1J1tSsw==',
    'searchSe': 'road',
    'srchwrd': '',
    'countPerPage': '10',
    'currentPage': '1'
}
params['srchwrd'] = srchwrd

response = requests.get(url, params=params).text.encode('utf-8')
xmlobj = BeautifulSoup(response, 'lxml-xml')

post_num = xmlobj.find_all('zipNo')
for i in post_num:
    print(i.text)

# address = xmlobj.find_all('lnmAdres')
# print(address.text)

print(len(post_num))
