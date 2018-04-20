from ceic.ceic_crawler import CEIC, Detail

if __name__ == '__main__':
    c = CEIC()
    c.crawler()
    d = Detail()
    d.get_url()
