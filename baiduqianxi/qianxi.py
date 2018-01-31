from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import pika
import pymongo
import datetime




def connect_mongodb(host, port, database, collection):
    client = pymongo.MongoClient(host, port, connect=False)
    db = client[database]
    coll = db.get_collection(collection)
    return coll


coll = connect_mongodb('192.168.0.235', 27017, 'crawler_dianping', 'url_list')
baiduqianxi = connect_mongodb('192.168.0.235', 27017, 'baiduqianxi', 'baiduqianxi')


def get_baiduqianxi(city_list):
    for city in city_list:
        # browser = webdriver.Chrome(executable_path='chromedriver.exe')
        browser = webdriver.PhantomJS()
        browser.get('http://qianxi.baidu.com/')
        try:
            time.sleep(5)
            elem = browser.find_element_by_id('input_cityName')
            elem.send_keys(city + Keys.RETURN)
            time.sleep(5)
            in_data = browser.find_element_by_class_name('div_list_container')
            in_info = in_data.text
            in_list = in_info.split('\n')
            in_dict = {}
            for i in in_list:
                print(i)
                list_ = i.split(' ')
                city_name = list_[1].replace(city, '')
                number = list_[2].replace('％', '')
                in_dict[city_name] = number

            print('---------')
            browser.find_elements_by_class_name('btn-group')[1].click()
            out_data = browser.find_element_by_class_name('div_list_container')
            out_info = out_data.text
            out_list = out_info.split('\n')
            out_dict = {}
            for i in out_list:
                list_ = i.split(' ')
                city_name = list_[1].replace(city, '')
                number = list_[2].replace('％', '')
                out_dict[city_name] = number
            baiduqianxi.insert_one({
                'city': city,
                'in': in_dict,
                'out': out_dict,
                'datetime': datetime.datetime.now()
            })
        except Exception as e:
            print(e)
        browser.close()

if __name__ == '__main__':
    city_list = ['衢州', '晋中', '锦州', '拉萨', '株洲', '黄南', '赤峰', '盘锦', '永州', '平顶山', '驻马店', '衡水', '山南', '厦门', '宁德', '徐州',
                 '抚顺', '安顺', '双鸭山', '南阳', '鞍山', '潮州', '鹰潭', '威海', '新余', '周口', '滨州', '廊坊', '南充', '临高', '石嘴山', '酒泉',
                 '西双版纳州', '乐东', '绍兴', '扬州', '张掖', '梧州', '崇左', '通辽', '济南', '潜江', '儋州', '河源', '庆阳', '赣州', '阜阳', '襄阳',
                 '常州', '辽阳', '南京', '内江', '长春', '怒江州', '三沙', '咸宁', '广元', '铜川', '金昌', '白沙', '阿拉尔', '乌鲁木齐', '沈阳', '大理',
                 '北京', '昌吉', '成都', '信阳', '临夏', '大兴安岭', '丽江', '商丘', '黔西南', '梅州', '东莞', '黔东南', '忻州', '宣城', '温州', '平凉',
                 '保定', '六盘水', '亳州', '玉溪', '包头', '湛江', '玉树州', '上海', '漯河', '吉安', '无锡', '哈尔滨', '三亚', '大同', '牡丹江', '丽水',
                 '鹤壁', '本溪', '铜仁', '泉州', '珠海', '张家界', '江门', '沧州', '晋城', '琼中', '重庆', '固原', '南通', '安庆', '九江', '鄂州', '太原',
                 '湖州', '惠州', '清远', '荆州', '合肥', '苏州', '湘潭', '运城', '武汉', '海西州', '图木舒克', '菏泽', '石家庄', '广安', '巴中', '钦州',
                 '濮阳', '聊城', '南平', '怀化', '汕尾', '曲靖', '定安', '青岛', '渭南', '延安', '枣庄', '邢台', '朝阳', '贵阳', '盐城', '琼海', '烟台',
                 '德阳', '那曲', '百色', '淮安', '鄂尔多斯', '朔州', '长治', '揭阳', '吐鲁番', '池州', '松原', '昌都', '新乡', '佛山', '眉山', '遂宁',
                 '镇江', '呼和浩特', '西宁', '大庆', '泰州', '南宁', '东方', '自贡', '文昌', '海东', '通化', '恩施', '普洱', '随州', '五家渠', '玉林',
                 '汉中', '贺州', '北海', '白山', '吕梁', '银川', '黑河', '韶关', '红河', '昭通', '和田', '宜昌', '郴州', '宿迁', '十堰', '六安', '呼伦贝尔',
                 '海口', '白城', '漳州', '海北州', '嘉兴', '克孜勒苏', '绵阳', '阿克苏', '莆田', '孝感', '景德镇', '中山', '林芝', '防城港', '神农架', '萍乡',
                 '潍坊', '嘉峪关', '昆明', '岳阳', '来宾', '阳泉', '临汾', '攀枝花', '巴音郭楞', '河池', '塔城', '吴忠', '达州', '茂名', '保亭', '蚌埠',
                 '贵港', '陇南', '日喀则', '克拉玛依', '陵水', '承德', '娄底', '阿里', '昌江', '仙桃', '衡阳', '马鞍山', '济宁', '阿勒泰', '伊犁', '郑州',
                 '五指山', '大连', '定西', '阳江', '汕头', '日照', '保山', '屯昌', '黄冈', '桂林', '吉林', '洛阳', '黄石', '毕节', '宜宾', '阜新', '邵阳',
                 '石河子', '常德', '澄迈', '云浮', '安阳', '葫芦岛', '张家口', '鹤岗', '淄博', '资阳', '长沙', '杭州', '福州', '临沂', '雅安', '益阳',
                 '伊春', '黄山', '咸阳', '焦作', '天津', '柳州', '唐山', '泸州', '广州', '丹东', '金华', '天水', '德州', '乐山', '邯郸', '泰安', '开封',
                 '乌海', '三明', '果洛州', '天门', '喀什', '湘西', '宝鸡', '黔南', '巴彦淖尔', '芜湖', '上饶', '哈密', '济源', '七台河', '佳木斯', '迪庆州',
                 '铜陵', '德宏州', '安康', '兰州', '四平', '舟山', '龙岩', '北屯', '许昌', '铁岭', '楚雄', '白银', '延边', '深圳', '秦皇岛', '辽源',
                 '乌兰察布', '营口', '莱芜', '西安', '万宁', '文山州', '鸡西', '肇庆', '淮北', '中卫', '甘南', '遵义', '三门峡', '绥化', '宁波', '南昌',
                 '滁州', '商洛']
    get_baiduqianxi(city_list)
