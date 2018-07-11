from baike_city.city_name import city_list
from lib.mongo import Mongo
import yaml
from lib.log import LogHandler
from lxml import etree
import requests
import os
import re

path = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
setting = yaml.load(open(path + '\\config.yaml'))
log = LogHandler('baidubaike')
connect = Mongo(setting['baidubaike']['mongo']['host']).connect
coll = connect[setting['baidubaike']['mongo']['db']][setting['baidubaike']['mongo']['collection']]

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'
}


def crawler_baike():
    data = {}
    for city in city_list:
        print(city)
        url_city = 'https://baike.baidu.com/item/' + city
        response = requests.get(url_city, headers=headers)
        html = response.content.decode('utf-8')
        tree = etree.HTML(html)
        key_list = tree.xpath('//div[@class="basic-info cmn-clearfix"]/dl/dt')
        for i in key_list:
            key = i.xpath('text()')[0].replace('\xa0', '').replace('\n', '')
            value = i.xpath('string(following-sibling::dd)').replace('\xa0', '').replace('\n', '')
            re_value = re.sub('\[\d+\]', '', value)
            data[key] = re_value
        print(data)
        data = {}


if __name__ == '__main__':
    crawler_baike()
