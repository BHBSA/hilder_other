# todo update

import requests
import re
from ceic.country import country
from dateutil import parser
from lib.mongo import Mongo
import random
import yaml
from lib.log import LogHandler

m = Mongo('192.168.0.235')
connect = m.connect

setting = yaml.load(open('config.yaml'))
db_name = setting['CEIC']['mongo']['db']
State_indicators_name = setting['CEIC']['mongo']['State_indicators']
State_indicators_details_name = setting['CEIC']['mongo']['State_indicators_details']
log = LogHandler('CEIC')

proxy = [{"http": "http://192.168.0.96:4234"},
         {"http": "http://192.168.0.93:4234"},
         {"http": "http://192.168.0.90:4234"},
         {"http": "http://192.168.0.94:4234"},
         {"http": "http://192.168.0.98:4234"},
         {"http": "http://192.168.0.99:4234"},
         {"http": "http://192.168.0.100:4234"},
         {"http": "http://192.168.0.101:4234"},
         {"http": "http://192.168.0.102:4234"},
         {"http": "http://192.168.0.103:4234"}, ]


class Detail:
    def create_date(self, indexFrequency, start_year, start_mouth, end_year, ):
        """

        :return: ['from=2016-1&to=2017-1', 'from=2016-1&to=2017-1', 'from=2016-1&to=2017-1', 'from=2016-1&to=2017-1',]
        """
        """
        根据开始时间分割年月日
        """
        if indexFrequency == '年':
            # print('年')
            s = [str(start_year) + '-' + str(start_mouth)]
            # print(start_year, end_year)
            while start_year < end_year:
                start_year = start_year + 11
                s.append(str(start_year) + '-' + str(start_mouth))
            # print(s)
        elif indexFrequency == '季':
            # print('季')
            s = [str(start_year) + '-' + str(start_mouth)]
            # print(start_year, end_year)
            while start_year < end_year:
                start_year = start_year + 2
                s.append(str(start_year) + '-' + str(start_mouth))
            # print(s)
        else:
            # print('月')
            s = [str(start_year) + '-' + '1']
            # print(start_year, end_year)
            while start_year < end_year:
                start_year = start_year + 1
                s.append(str(start_year) + '-' + '1')
            complete_url_list = []
            for i in range(0, len(s) - 1):
                complete_url_list.append('from=' + s[i] + '&' + 'to=' + s[i] + '2')
            # log.info('complete_url_list', complete_url_list)
            return complete_url_list
            # print(s)
        # from=2016-1&to=2017-1
        complete_url_list = []
        for i in range(0, len(s) - 1):
            complete_url_list.append('from=' + s[i] + '&' + 'to=' + s[i + 1])
        log.info('complete_url_list', complete_url_list)
        return complete_url_list

    def get_url(self):
        # collection = connect['test']['ecic']
        collection = connect[db_name][State_indicators_name]
        for info in collection.find():
            """
            info :
            {
                "_id" : ObjectId("5ad8389685699237a0c8ae90"),
                "indexUpdate" : "2018-03-28",
                "indexFrequency" : "季",
                "indexEnName" : "nominal-gdp",
                "indexEnd" : "2017-12",
                "url" : "https://www.ceicdata.com/zh-hans/indicator/united-states/nominal-gdp",
                "indexStart" : "1947-03",
                "indexName" : "名义国内生产总值",
                "indexCategory" : "国民经济核算",
                "indexUnit" : "百万美元",
                "countryName" : "美国",
                "countryEnName" : "united-states"
            }
            """
            countryEnName = info['countryEnName']
            indexEnName = info['indexEnName']

            indexStart = info['indexStart']
            indexEnd = info['indexEnd']
            indexFrequency = info['indexFrequency']

            start_year = int(indexStart.split('-')[0])
            start_mouth = int(indexStart.split('-')[1])

            end_year = int(indexEnd.split('-')[0])
            end_mouth = int(indexEnd.split('-')[1])
            # print(start_year, start_mouth, end_year, end_mouth)

            url_list = self.create_date(indexFrequency, start_year, start_mouth, end_year, )

            url = info['url']

            while True:
                try:
                    proxy_ = proxy[random.randint(0, 9)]
                    res = requests.get(url=url, proxies=proxy_)
                    if res.status_code == 200:
                        break
                except Exception as e:
                    log.info('请求出错，url={}，proxy={}，'.format(url, proxy_), e)
            city_type = re.search('<img src="https://www.ceicdata.com/.*?/.*?/(.*?)/', res.content.decode(),
                                  re.S | re.M).group(1)
            for i in url_list:
                url = 'https://www.ceicdata.com/datapage/charts/' + city_type + '?type=column&' + i + '&width=1500&height=700'
                # print(url)

                while True:
                    try:
                        proxy_ = proxy[random.randint(0, 9)]
                        res = requests.get(url=url, proxies=proxy_)
                        if res.status_code == 200:
                            break
                    except Exception as e:
                        log.info('请求出错，url={}，proxy={}，'.format(url, proxy_), e)

                # print(res.content.decode())
                self.parse_detail(res.content.decode(), url, countryEnName, indexEnName)
            break

    @staticmethod
    def parse_detail(html, url, countryEnName, indexEnName):
        data_info_list = re.search('<g class="highcharts-axis-labels highcharts-xaxis-labels ">(.*?)</g>', html,
                                   re.S | re.M).group(1)
        date_list = []
        for i in re.findall('<tspan>(.*?)</tspan>', data_info_list, re.S | re.M):
            date_list.append(i)

        num_list = []
        num_info_list = re.findall('<g class="highcharts-label highcharts-data-label(.*?)</g>', html, re.S | re.M)
        for k in num_info_list:
            value_ = re.search('<tspan .*?>(.*?)</tspan>', k, re.S | re.M).group(1)
            num_list.append(value_)

        if len(date_list) != len(num_list):
            log.error('页面的数据和月份对应不上date_list={},num_list={}, url={},'.format(len(date_list), len(num_list), url))
            return

        for j in range(0, len(date_list)):
            num = re.search('\d+', date_list[j], re.S | re.M).group(0)
            list_time = date_list[j].split('\'')

            """
            判断是19世纪还是20世纪
            """
            if int(num) > 20:
                date_list[j] = list_time[0] + '19' + list_time[1]
            else:
                date_list[j] = list_time[0] + '20' + list_time[1]
            # collection = connect['test']['State_indicators_details']
            collection = connect[db_name][State_indicators_details_name]
            collection.insert_one({
                'countryEnName': countryEnName,
                'indexEnName': indexEnName,
                'Date': parser.parse(date_list[j]).strftime('%Y-%m'),
                'Value': num_list[j],
            })


class CEIC:
    """
    列表页面所有种类和信息
    """

    def __init__(self):
        self.countries_url = 'https://www.ceicdata.com/zh-hans/countries'

    def crawler(self):

        while True:
            try:
                proxy_ = proxy[random.randint(0, 9)]
                res = requests.get(url=self.countries_url, proxies=proxy_)
                if res.status_code == 200:
                    break
            except Exception as e:
                log.info('请求出错，url={}，proxy={}，'.format(self.countries_url, proxy_), e)

        # print(res.content.decode())
        country_list = []
        for url in re.findall('<a href="(/zh-hans/country/.*?)"', res.content.decode(), re.S | re.M):
            country_list.append('https://www.ceicdata.com' + url)

        for i in country_list:
            self.crawler_list_page(i)

    def crawler_list_page(self, url):
        # print('url={}'.format(url))
        while True:
            try:
                proxy_ = proxy[random.randint(0, 9)]
                res = requests.get(url=url, proxies=proxy_)
                if res.status_code == 200:
                    break
            except Exception as e:
                log.info('请求出错，url={}，proxy={}，'.format(self.countries_url, proxy_), e)
        html_str = res.content.decode()
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

            url = re.search('<a href="(.*?)"', info, re.S | re.M).group(1)

            # collection = connect['test']['State_indicators']
            collection = connect[db_name][State_indicators_name]
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
                'url': 'https://www.ceicdata.com' + url
            })
        log.info('{}国家已经结束'.format(countryName))
