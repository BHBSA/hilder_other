import pymongo
import requests

client = pymongo.MongoClient('192.168.0.61', 27017)
db = client['buildings']
coll_community = db.get_collection('community_image_url')
coll_house = db.get_collection('images_community_house')
count = 0
for i in coll_community.find({},no_cursor_timeout = True):
    for img in i['img_list']:
        response = requests.get(url=img['img'])
        if response.status_code == 200:
            count += 1
            print(count)
        else:
            print(response.url)
for i in coll_house.find():
    for img in i['img_list']:
        response = requests.get(url=img['img'])
        if response.status_code == 200:
            count += 1
            print(count)
        else:
            print(response.url)
