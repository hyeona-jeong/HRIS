import requests
import pprint
import json

url = 'http://openapi.epost.go.kr/postal/retrieveNewAdressAreaCdService/retrieveNewAdressAreaCdService/getNewAddressListAreaCd'
params = {
    'serviceKey': '7kEsxVN9P4SCOTTBAmWPvKJQDrhW4i08XbJe98mkPpthjKeB6bQjiDMSEJuNHVroSg3sx8OUYLaeSIe1J1tSsw==',
    'searchSe': 'dong',
    'srchwrd': '주월동 408-1',
    'countPerPage': '10',
    'currentPage': '1'
}

response = requests.get(url, params=params)
contents = response.text

pp = pprint.PrettyPrinter(indent=4)
pp.pprint(contents)
