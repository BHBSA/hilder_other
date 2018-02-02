"""
百度迁徙
requests
"""
import requests
import re
from .city_list import CITY_LIST
import datetime
from lib.mongo import Mongo
from queue import Queue


class Baiduqianxi:
    m = Mongo('192.168.0.235', 27017, 'baiduqianxi', 'baiduqianxi_test')
    coll = m.get_collection_object()
    now_time = datetime.datetime.now()
    today_int = int(now_time.strftime('%Y%m%d'))
    q = Queue()

    def put_in_queue(self):
        for city_name in CITY_LIST:
            self.q.put(city_name)

    def start_consume(self):
        count = 0
        self.put_in_queue()
        while not self.q.empty():
            city_name = self.q.get()
            try:
                proxies = {
                    'http': '192.168.0.90:4234'
                }
                type_ = 'migrate_in'
                city = city_name
                timeStr = str(self.today_int)
                url = 'http://qianxi.baidu.com/api/city-migration.php?callback=abc&type=' + type_ + '&sort_by=low_index&limit=10&city_name=' + city + '&date_start=' + timeStr + '&date_end=' + timeStr
                res_in = requests.get(url, proxies=proxies)
                in_info = re.search(r'\[(.*?)\]', res_in.text).group()
                in_list = eval(in_info)
                in_all_list = []
                for i in in_list:
                    in_all_list.append(i)
                type_ = 'migrate_out'
                url = 'http://qianxi.baidu.com/api/city-migration.php?callback=abc&type=' + type_ + '&sort_by=low_index&limit=10&city_name=' + city + '&date_start=' + timeStr + '&date_end=' + timeStr
                res_out = requests.get(url, proxies=proxies)
                out_info = re.search(r'\[(.*?)\]', res_out.text).group()
                out_list = eval(out_info)
                out_all_list = []
                for i in out_list:
                    out_all_list.append(i)
                count += 1
                print(count, city_name)
                data = {
                    'city': city_name,
                    'date': int(timeStr),
                    'insert_time': datetime.datetime.now(),
                    'in': in_all_list,
                    'out': out_all_list,
                }
                if not in_all_list and not in_all_list:
                    print('in and out is null')
                else:
                    self.coll.insert_one(data)
            except Exception as e:
                print('错误')
                self.q.put(city_name)
