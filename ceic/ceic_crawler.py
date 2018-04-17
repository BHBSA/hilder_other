import requests
import re
from country import country
from dateutil import parser
from lib.mongo import Mongo

m = Mongo('192.168.0.235')
connect = m.connect


class CEIC:
    def __init__(self):
        self.countries_url = 'https://www.ceicdata.com/zh-hans/countries'
        self.proxy = {
            'https': '192.168.0.90:4234'
        }

    def crawler(self):
        res = requests.get(url=self.countries_url, proxies=self.proxy)
        # print(res.content.decode())
        country_list = []
        for url in re.findall('<a href="(/zh-hans/country/.*?)"', res.content.decode(), re.S | re.M):
            country_list.append('https://www.ceicdata.com' + url)

        for i in country_list:
            self.crawler_list_page(i)

    def crawler_list_page(self, url):
        print('url={}'.format(url))
        html_str = requests.get(url, proxies=self.proxy).content.decode()
        countryName = re.search('<h1 class="datapage-header">(.*?)</h1>', html_str, re.S | re.M).group(1)
        countryEnName = country[countryName]
        for info in re.findall('<tr class="datapage-table-row " >.*?</tr>', html_str, re.S | re.M):
            indexCategory = re.search('<td class="name-cell".*?data-th="(.*?)"', info, re.S | re.M).group(1)
            indexEnName = re.search('<a href="/.*?/.*?/.*?/(.*?)"', info, re.S | re.M).group(1)
            indexName = re.search('<a href="/.*?/.*?/.*?/.*?".*?title="(.*?)">', info, re.S | re.M).group(1)

            # 时间格式化
            start_time = re.search('范围.*?<p>(.*?)-.*?</p>', info, re.S | re.M).group(1)
            indexStart = parser.parse(start_time).strftime('%Y-%m')
            end_time = re.search('范围.*?<p>.*?-(.*?)</p>', info, re.S | re.M).group(1)
            indexEnd = parser.parse(end_time).strftime('%Y-%m')

            indexFrequency = re.search('frequency.*?data-value="(.*?)">', info, re.S | re.M).group(1)
            indexUnit = re.search('data-th="单位".*?<p>(.*?)</p>', info, re.S | re.M).group(1)
            indexUpdate = re.search('范围.*?<small>于(.*?)更新</small>', info, re.S | re.M).group(1)

            collection = connect['test']['ecic']
            collection.insert_one({
                'countryName': countryName,
                'countryEnName': countryEnName,

                'indexCategory': indexCategory,
                'indexEnName': indexEnName,
                'indexName': indexName,
                'indexStart': indexStart,
                'indexEnd': indexEnd,
                'indexFrequency': indexFrequency,
                'indexUnit': indexUnit,
                'indexUpdate': indexUpdate,
            })
        print('{}城市已经结束'.format(countryName))


if __name__ == '__main__':
    c = CEIC()
    c.crawler()
