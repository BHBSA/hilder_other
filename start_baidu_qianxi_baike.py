from baiduqianxi.qianxi import Baiduqianxi
import schedule
from baike_city.baike import crawler_baike

if __name__ == '__main__':
    b = Baiduqianxi()
    schedule.every().day.at("12:00").do(b.start_consume)
    schedule.every().sunday.at("12:00").do(crawler_baike)
    while True:
        schedule.run_pending()
        schedule.run_pending()