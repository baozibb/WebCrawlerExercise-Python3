# -*- coding:utf-8  -*-
# import env  # 设置环境变量
from proxypool.crawlers.base import BaseCrawler
from proxypool.schemas.proxy import Proxy
from pyquery import PyQuery as pq


BASE_URL = 'http://www.ip3366.net/?stype=1&page={page}'
MAX_PAGE = 10


class IP3366Crawler(BaseCrawler):
    '''
    ip3366 crawler, http://www.ip3366.net/
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
        ips = doc('table tbody tr').items()
        for ip in ips:
            host = ip.find('td:first-child').text().strip()
            port = ip.find('td:nth-child(2)').text().strip()
            proxy = Proxy(host=host, port=port)
            yield proxy


if __name__ == '__main__':
    crawler = IP3366Crawler()
    for proxy in crawler.crawl():
        print(proxy)
