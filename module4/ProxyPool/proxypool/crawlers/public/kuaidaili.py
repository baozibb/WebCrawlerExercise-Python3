# -*- coding:utf-8  -*-
# import env  # 设置环境变量
from proxypool.crawlers.base import BaseCrawler
from proxypool.schemas.proxy import Proxy
from pyquery import PyQuery as pq

# 快代理的国内高匿代理
BASE_URL = 'https://www.kuaidaili.com/free/inha/{page}/'
MAX_PAGE = 200


class KuaidailiCrawler(BaseCrawler):
    '''
    kuaidaili crawler, https://www.kuaidaili.com/
    '''
    urls = [BASE_URL.format(page=page) for page in range(1, MAX_PAGE + 1)]

    def parse(self, html):
        '''parse html file to get proxies
        :param html: the text of website
        :type html: str

        :return: the generator of proxies
        :rtype: Proxy
        '''
        doc = pq(html)
        for item in doc('table tr').items():
            td_ip = item.find('td[data-title="IP"]').text().strip()
            td_port = item.find('td[data-title="PORT"]').text().strip()
            if td_ip and td_port:
                yield Proxy(host=td_ip, port=td_port)


if __name__ == '__main__':
    crawler = KuaidailiCrawler()
    for proxy in crawler.crawl():
        print(proxy)
