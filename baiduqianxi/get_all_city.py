import pymongo
import pika
def connect_mongodb(host, port, database, collection):
    client = pymongo.MongoClient(host, port,connect=False)
    db = client[database]
    coll = db.get_collection(collection)
    return coll


def connect_rabbit(host, queue):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=host, ))
    channel = connection.channel()
    channel.queue_declare(queue=queue)
    return channel
coll = connect_mongodb('192.168.0.235', 27017, 'crawler_dianping', 'url_list')
channel = connect_rabbit('192.168.0.235', 'baiduqianxi_all_city')
for i in coll.find():
    city = i['city']
    print(city)
    channel.basic_publish(exchange='',
                          routing_key='baiduqianxi_all_city',
                          body=city,
                          )