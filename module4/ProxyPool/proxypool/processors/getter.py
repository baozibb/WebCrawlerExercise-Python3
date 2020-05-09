# -*- coding:utf-8  -*-
# import env  # 设置环境变量
from loguru import logger
from proxypool.storages.store_by_redis import RedisClient
from proxypool.setting import PROXY_NUMBER_MAX
from proxypool.crawlers import __all__ as crawlers_cls


class Getter(object):
    ''' 代理池的 Getter '''
    def __init__(self):
        ''' 初始化数据库和爬虫 '''
        self.redis = RedisClient()
        self.crawlers_cls = crawlers_cls
        self.crawlers = [crawlers_cls() for crawlers_cls in self.crawlers_cls]

    def is_full(self):
        ''' 判断代理池是否已满 '''
        return self.redis.count() >= PROXY_NUMBER_MAX

    @logger.catch
    def run(self):
        ''' 运行爬虫获取代理 '''
        if self.is_full():
            return
        for crawler in self.crawlers:
            for proxy in crawler.crawl():
                self.redis.add(proxy)


if __name__ == '__main__':
    getter = Getter()
    getter.run()
