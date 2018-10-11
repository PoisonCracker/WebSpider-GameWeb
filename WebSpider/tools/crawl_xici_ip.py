import requests
from fake_useragent import UserAgent
from scrapy.selector import Selector
import MySQLdb

# conn = MySQLdb.connect(host='localhost', user='root', passwd='root', db='webspider', charset='utf8')
# cousor = conn.cursor()
ua = UserAgent()


def crewl_ips():
    headers = {"User-Agent": ua.random}
    for i in range(1568):
        res = requests.get('http://www.xicidaili.com/nn/{0}'.format(i), headers=headers)

    selector = Selector(text=res.text)
    all_attr = selector.css('#ip_list tr')
    print(all_attr)
    ip_list = []
    for tr in all_attr[1:]:
        speed_str = tr.css('.bar::attr(title)').extract()[0]
        if speed_str:
            speed = float(speed_str.split('秒')[0])
        all_text = tr.css('td::text').extract()

        ip = all_text[0]
        port = all_text[1]
        proxy_type = all_text[5]
        time = all_text[10]
        print(ip)
        ip_list.append((ip, port, proxy_type, speed, time))
        print(ip_list)
        # for ip_info in ip_list:
        #     cousor.execute(
        #         "insert ip_list(ip,port,speed,proxy_type,time) VALUES('{0} ','{1}','{2}','{3}','{4}')"
        #         (ip_info[0], ip_info[1], ip_info[2], ip_info[3], ip_info[4])
        #     )
        #     conn.commit()


crewl_ips()
