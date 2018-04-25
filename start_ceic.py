from ceic.detail import Detail
from ceic.ceic_crawler import CEIC
from multiprocessing import Process
import schedule

if __name__ == '__main__':
    # # 开启 ceic 首页
    # c = CEIC()
    # c.crawler()

    # 开启ceic详情
    d = Detail()
    for i in range(10):
        Process(target=d.get_url).start()

