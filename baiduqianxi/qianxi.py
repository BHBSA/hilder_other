from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import datetime
from lib.mongo import Mongo
from city_list import city_list


def get_baiduqianxi(city_list):
    browser = webdriver.ChromeOptions()
    browser.add_argument('--headless')
    browser = webdriver.Chrome(chrome_options=browser, executable_path='chromedriver.exe')
    browser.set_window_size(1600, 900)
    m = Mongo('192.168.0.235', 27017, 'baiduqianxi', 'baiduqianxi_test')
    coll = m.get_collection_object()

    for city in city_list:
        browser.get('http://qianxi.baidu.com/')
        try:
            time.sleep(3)
            elem = browser.find_element_by_id('input_cityName')
            elem.send_keys(city)
            time.sleep(1)
            browser.find_element_by_class_name('input-group-addon').click()
            time.sleep(5)
            in_data = browser.find_element_by_class_name('div_list_container')
            in_info = in_data.text
            print(in_info)
            in_list = in_info.split('\n')
            in_dict = {}
            for i in in_list:
                list_ = i.split(' ')
                city_name = list_[1].replace(city, '')
                number = list_[2].replace('％', '')
                in_dict[city_name] = number
            print('---------')
            browser.find_element_by_css_selector('body > div.content-wrap > div.content-main > div.list-wrap > div.sortList-warp > div > div.button-box.b1.tab_china_move.drawMap > span:nth-child(2) > a').click()
            out_data = browser.find_element_by_class_name('div_list_container')
            out_info = out_data.text
            print(out_info)
            out_list = out_info.split('\n')
            out_dict = {}
            for i in out_list:
                list_ = i.split(' ')
                city_name = list_[1].replace(city, '')
                number = list_[2].replace('％', '')
                out_dict[city_name] = number
            coll.insert_one({
                'city': city,
                'in': in_dict,
                'out': out_dict,
                'datetime': datetime.datetime.now()
            })
        except Exception as e:
            print(e)
            print(city)


if __name__ == '__main__':
    # print(city_list)
    get_baiduqianxi(city_list)
