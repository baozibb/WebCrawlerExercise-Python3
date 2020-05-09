# -*- coding:utf-8  -*-
from retrying import retry
import requests
from loguru import logger
import random


class BaseCrawler(object):
    USER_AGENT_LIST = [
        'MSIE (MSIE 6.0; X11; Linux; i686) Opera 7.23',
        'Opera/9.20 (Macintosh; Intel Mac OS X; U; en)',
        'Opera/9.0 (Macintosh; PPC Mac OS X; U; en)',
        'iTunes/9.0.3 (Macintosh; U; Intel Mac OS X 10_6_2; en-ca)',
        'Mozilla/4.76 [en_jp] (X11; U; SunOS 5.8 sun4u)',
        'iTunes/4.2 (Macintosh; U; PPC Mac OS X 10.2)',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:5.0) Gecko/20100101 Firefox/5.0',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:9.0) Gecko/20100101 Firefox/9.0',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:16.0) Gecko/20120813 Firefox/16.0',
        'Mozilla/4.77 [en] (X11; I; IRIX;64 6.5 IP30)',
        'Mozilla/4.8 [en] (X11; U; SunOS; 5.7 sun4u)',
        'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML,like Gecko) Chrome/67.0.3396.62 Safari/537.36'
    ]
    urls = []  # 网站的列表页（即包含 IP 的网页）

    # 定义重试次数
    @retry(stop_max_attempt_number=3, retry_on_result=lambda x: x is None)
    def fetch(self, url, **kwargs):
        ''' 爬取 url '''
        headers = {
            "Host": "www.xicidaili.com",
            "User-Agent": random.choice(self.USER_AGENT_LIST),
        }
        try:
            response = requests.get(url, headers=headers, **kwargs)
            if response.status_code == requests.codes.ok:
                return response.text
        except requests.ConnectionError:
            return

    @logger.catch
    def crawl(self):
        ''' 爬取网站的主函数 '''
        for url in self.urls:
            logger.info(f'fetching {url}')
            html = self.fetch(url)
            for proxy in self.parse(html):
                logger.info(f'fetched proxy {proxy.string()} from {url}')
                yield proxy
