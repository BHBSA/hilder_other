import requests
import urllib
import re

cities = ['上海', '萍乡']
headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Cookie': 'BAIDUID=98C2249E28948F3E040B59450E9F1ED2:FG=1; BIDUPSID=98C2249E28948F3E040B59450E9F1ED2; PSTM=1514361799; Hm_lvt_55b574651fcae74b0a9f1cf9c8d7c93a=1523269340; Hm_lpvt_55b574651fcae74b0a9f1cf9c8d7c93a=1523269340; pgv_pvi=1332027392; pgv_si=s3426598912',
    'Host': 'baike.baidu.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'
}
for city in cities:
    i = urllib.parse.quote(city)
    url = 'https://baike.baidu.com/item/' + i
    # print(url)
    res = requests.get(url=url, headers=headers)
    html = res.content.decode('UTF-8', 'ignore')

    # 中文名称
    chinese_name = re.search(r'中文名称</dt>(.*?)<dd(.*?)>(.*?)</dd>', html, re.S | re.M).group(3).strip()
    print('中文名称', chinese_name)

    # 外文名称
    foreign_names = re.search(r'外文名称</dt>(.*?)<dd(.*?)>(.*?)</dd>', html, re.S | re.M).group(3).strip()
    print('外文名称', foreign_names)

    # 别名
    alias = re.search(r'别&nbsp;&nbsp;&nbsp;&nbsp;名.*?<dd.*?>(.*?)</dd>', html, re.S | re.M).group(1).strip()
    if '<a' in alias:
        alias = re.findall(r'<a.*?>(.*?)<', alias)
        alias = ('、').join(alias)
    print('别名', alias)

    # 行政区划(Administrative_categories)
    admini_cate = re.search(r'行政区类别</dt>.*?<dd.*?>(.*?)</dd>', html, re.S | re.M).group(1).strip()
    if '<a' in admini_cate:
        admini_cate = re.findall(r'<a.*?>(.*?)<', admini_cate, re.S | re.M)
        admini_cate = ''.join(admini_cate)
    print(admini_cate)

    # 所属地区(Attribution_area)
    attr_area = re.search(r'所属地区</dt>.*?<dd.*?>(.*?)</dd>', html, re.S | re.M).group(1).strip()
    print(attr_area)

    # 下辖地区(governs_area)
    gov_area = re.search(r'下辖地区</dt>.*?<dd.*?>(.*?)</dd>', html, re.S | re.M).group(1).strip()
    if '<a' in gov_area:
        gov_area = re.findall(r'<a.*?>(.*?)<', gov_area)
        gov_area = ('、').join(gov_area)
    print(gov_area)

    # 政府驻地
    government_post = re.search(r'政府驻地</dt>.*?<dd.*?>(.*?)</dd>', html, re.S | re.M).group(1).strip()
    print(government_post)

    # 电话区号(Telephone_code)
    tel_code = re.search(r'电话区号</dt>.*?<dd.*?>(.*?)</dd>', html, re.S | re.M).group(1).strip()
    print(tel_code)

    # 邮政区码
    postal_code = re.search(r'邮政区码</dt>.*?<dd.*?>(.*?)</dd>', html, re.S | re.M).group(1).strip()
    print(postal_code)

    # 地理位置(geographical_position)
    geo_position = re.search(r'地理位置</dt>.*?<dd.*?>(.*?)</dd>', html, re.S | re.M).group(1).strip()
    if '<a' in geo_position:
        geo_position = re.findall(r'<a.*?>(.*?)<', geo_position)
        geo_position = ''.join(geo_position)
    print(geo_position)

    # 面积
    area = re.search(r'面&nbsp;&nbsp;&nbsp;&nbsp;积</dt>.*?<dd.*?>(.*?)</dd>', html, re.S | re.M).group(1).strip()
    print(area)

    # 人口
    population = re.search(r'人&nbsp;&nbsp;&nbsp;&nbsp;口.*?<dd.*?>(.*?)<', html, re.S | re.M).group(1).strip()
    print('人口', population)

    # 方言
    dialect = re.search(r'方&nbsp;&nbsp;&nbsp;&nbsp;言</dt>.*?<dd.*?>(.*?)</dd>', html, re.S | re.M).group(1).strip()
    if '<a' in dialect:
        dialect = re.search(r'<a.*?>(.*?)</a>(.*?)<a.*?>(.*?)</a>', dialect).group()
        dialect = str(dialect)
    print(dialect)

    # 气候条件(Climatic_conditions)
    climatic_conditions = re.search(r'气候条件</dt>.*?<dd.*?>(.*?)</dd>', html, re.S | re.M).group(1).strip()
    if '<a' in climatic_conditions:
        climatic_conditions = re.findall(r'<a.*?>(.*?)<', climatic_conditions)
        climatic_conditions = ''.join(climatic_conditions)
    print(climatic_conditions)

    # 著名景点
    famous_scenery = re.search(r'著名景点</dt>.*?<dd.*?>(.*?)</dd>', html, re.S | re.M).group(1).strip()
    if '<a' in famous_scenery:
        famous_scenery = re.findall(r'<a.*?>(.*?)</a>(.*?)<a.*?>(.*?)</a>', famous_scenery)
    print(famous_scenery)

    # 机场
    airport = re.search(r'机&nbsp;&nbsp;&nbsp;&nbsp;场</dt>.*?<dd.*?>(.*?)</dd>', html, re.S | re.M).group(1).strip()
    if '<a' in airport:
        airport = re.findall(r'<a.*?>(.*?)</a>(.*?)<a.*?>(.*?)</a>', airport)
    print(airport)

    # 火车站
    railway_station = re.search(r'火车站</dt>.*?<dd.*?>(.*?)</dd>', html, re.S | re.M).group(1).strip()
    if '<a' in railway_station:
        railway_station = re.findall(r'<a.*?>(.*?)</a>(.*?)<a.*?>(.*?)</a>', railway_station)
    print(railway_station)

    # 车牌代码
    license_code = re.search(r'车牌代码</dt>.*?<dd.*?>(.*?)</dd>', html, re.S | re.M).group(1).strip()
    print(license_code)

    # 地区生产总值（Gross regional product）
    GRP = re.search(r'地区生产总值</dt>.*?<dd.*?>(.*?)</dd>', html, re.S | re.M).group(1).strip()

    # 人均生产总值
    GNPP = re.search(r'人均生产总值</dt>.*?<dd.*?>(.*?)</dd>', html, re.S | re.M).group(1).strip()

    # 人均支配收入（Per capita income）
    Per_capita_income = re.search(r'人均支配收入</dt>.*?<dd.*?>(.*?)<sup', html, re.S | re.M).group(1).strip()

    # 消费品零售额
    consu = re.search(r'消费品零售额</dt>.*?<dd.*?>(.*?)<sup', html, re.S | re.M).group(1).strip()
    print(consu)

    # 住户存款总额
    Total_household_deposits = re.search(r'住户存款总额</dt>.*?<dd.*?>(.*?)<sup', html, re.S | re.M).group(1).strip()

    # 市树市花
    Were_flower = re.search(r'市树市花</dt>.*?<dd.*?>(.*?)</dd>', html, re.S | re.M).group(1).strip()

    # 著名高校
    Famous_universities = re.search(r'著名高校</dt>.*?<dd.*?>(.*?)</dd>', html, re.S | re.M).group(1).strip()

    # 市委书记
    municipal_party_secretary = re.search('市委书记</dt>.*?<dd.*?>(.*?)</dd>', html, re.S | re.M).group(1).strip()
    print(municipal_party_secretary)

    # 市长
    mayor = tree.xpath('normalize-space(string(//dl[@class="basicInfo-block basicInfo-right"]/dd[12]))')
    print(mayor)
    # 行政代码
    Administrative_code = tree.xpath('normalize-space(string(//dl[@class="basicInfo-block basicInfo-right"]/dd[13]))')
    print(Administrative_code)
    # 城市精神
    City_spirit = tree.xpath('normalize-space(string(//dl[@class="basicInfo-block basicInfo-right"]/dd[14]))')
    print(City_spirit)
    # 人类发展指数
    Human_development_index = tree.xpath(
        'normalize-space(string(//dl[@class="basicInfo-block basicInfo-right"]/dd[15]))')
    print(Human_development_index)
    # 城市简称
    City_abbreviation = tree.xpath('normalize-space(string(//dl[@class="basicInfo-block basicInfo-right"]/dd[16]))')
    print(City_abbreviation)
