from ceic.ceic_crawler import CEIC, Detail
import schedule

if __name__ == '__main__':
    c = CEIC()
    c.crawler()
    d = Detail()
    d.get_url()
