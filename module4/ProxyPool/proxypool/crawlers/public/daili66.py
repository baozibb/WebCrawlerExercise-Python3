# -*- coding:utf-8  -*-
# import env  # 设置环境变量
from pyquery import PyQuery as pq
from proxypool.schemas.proxy import Proxy
from proxypool.crawlers.base import BaseCrawler

BASE_URL = 'http://www.66ip.cn/{page}.html'
MAX_PAGE = 200


class Daili66Crawler(BaseCrawler):
    '''
    daili66 crawler, http://www.66ip.cn/
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
        trs = doc('.containerbox table tr:gt(0)').items()
        for tr in trs:
            host = tr.find('td:nth-child(1)').text().strip()
            port = tr.find('td:nth-child(2)').text().strip()
            yield Proxy(host=host, port=port)


if __name__ == '__main__':
    crawler = Daili66Crawler()
    for proxy in crawler.crawl():
        print(proxy)
