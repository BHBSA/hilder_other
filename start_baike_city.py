from baike_city.baike import baike
import schedule

if __name__ == '__main__':
    schedule.every().sunday.at("12:00").do(baike)
    while True:
        schedule.run_pending()

