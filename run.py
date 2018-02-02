from baiduqianxi.qianxi import Baiduqianxi
import schedule

if __name__ == '__main__':
    b = Baiduqianxi()
    schedule.every().day.at("12:00").do(b.start_consume)
    while True:
        schedule.run_pending()
