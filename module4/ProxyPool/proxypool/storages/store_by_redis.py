# -*- coding:utf-8  -*-
# import env  # 设置环境变量
import redis
from proxypool.exceptions.empty import PoolEmptyException
from proxypool.schemas.proxy import Proxy
from proxypool.setting import REDIS_HOST, REDIS_PORT, REDIS_PASSWORD,\
     REDIS_KEY, PROXY_SCORE_MAX, PROXY_SCORE_MIN, PROXY_SCORE_INIT
from random import choice
from typing import List
from loguru import logger
from proxypool.utils.proxy import is_valid_proxy, convert_proxy_or_proxies

REDIS_CLIENT_VERSION = redis.__version__
IS_REDIS_VERSION_2 = REDIS_CLIENT_VERSION.startswith('2.')


class RedisClient(object):
    '''
    代理池的 redis 连接
    '''
    def __init__(self,
                 host=REDIS_HOST,
                 port=REDIS_PORT,
                 password=REDIS_PASSWORD,
                 **kwargs):
        '''
        初始化 redis 客户端
        :param host: redis host
        :param port: redis port
        :param password: redis password
        '''
        self.db = redis.StrictRedis(host=host,
                                    port=port,
                                    password=password,
                                    decode_responses=True,
                                    **kwargs)

    def add(self, proxy: Proxy, score=PROXY_SCORE_INIT) -> int:
        '''
        将代理加到 redis 中，并设置初始分数
        :param proxy: 代理，格式 ip:port, 例如 8.8.8.8:888
        :param score: 代理初始化的分数
        :type score: int
        :return: 成功添加的数量
        '''
        if not is_valid_proxy(f'{proxy.host}:{proxy.port}'):
            logger.info(f'invalid proxy {proxy}, throw it')
            return
        # if not self.db.exists(proxy):
        # 将代理添加到有序集合中
        if IS_REDIS_VERSION_2:
            return self.db.zadd(REDIS_KEY, score, proxy.string())
        return self.db.zadd(REDIS_KEY, {proxy.string(): score})

    def random(self) -> Proxy:
        '''
        获取随机代理
        1. 最开始，尝试获取最大分数的代理
        2. 如果不存在， 尝试通过排行榜获取
        3. 如果还是不存在，报错
        :return: proxy, like 8.8.8.8:888
        '''
        # 1. 尝试获取最大分数的代理
        proxies = self.db.zrangebyscore(REDIS_KEY, PROXY_SCORE_MAX,
                                        PROXY_SCORE_MAX)
        if len(proxies):
            return convert_proxy_or_proxies(choice(proxies))
        # 没有的话，通过排名获取
        proxies = self.db.zrangebyscore(REDIS_KEY, PROXY_SCORE_MIN,
                                        PROXY_SCORE_MAX)
        if len(proxies):
            return convert_proxy_or_proxies(choice(proxies))
        # 如果都没有, 报错
        raise PoolEmptyException

    def decrease(self, proxy: Proxy) -> int:
        '''
        降低代理的分数，如果比最小值还低，则删除
        :param proxy: proxy
        :return: new score
        '''
        score = self.db.zscore(REDIS_KEY, proxy.string())
        # 当前分数比最小值大
        if score and score > PROXY_SCORE_MIN:
            logger.info(f'{proxy.string()} current score {score}, decrease 1')
            if IS_REDIS_VERSION_2:
                return self.db.zincrby(REDIS_KEY, proxy.string(), -1)
            return self.db.zincrby(REDIS_KEY, -1, proxy.string())
        # 当前分数比最小值小
        else:
            logger.info(f'{proxy.string()} current score {score}, remove')
            return self.db.zrem(REDIS_KEY, proxy.string())

    def max(self, proxy: Proxy) -> int:
        '''
        将代理分数设成最大
        :param proxy: 代理
        :return: 新的分数
        '''
        logger.info(f'{proxy.string()} is valid, set to {PROXY_SCORE_MAX}')
        if IS_REDIS_VERSION_2:
            return self.db.zadd(REDIS_KEY, PROXY_SCORE_MAX, proxy.string())
        return self.db.zadd(REDIS_KEY, {proxy.string(): PROXY_SCORE_MAX})

    def count(self) -> int:
        '''
        获取代理的数量
        :return: 数量
        :rtype: int
        '''
        return self.db.zcard(REDIS_KEY)

    def all(self) -> List[Proxy]:
        '''
        获取所有代理
        :return: 代理列表
        '''
        return convert_proxy_or_proxies(
            self.db.zrangebyscore(REDIS_KEY, PROXY_SCORE_MIN, PROXY_SCORE_MAX))

    def batch(self, start, end) -> List[Proxy]:
        '''
        获取一批特定区间中的代理
        :param start: 代理的起始索引
        :param end: 代理的结束索引
        :return: 代理列表
        '''
        return convert_proxy_or_proxies(
            self.db.zrevrange(REDIS_KEY, start, end - 1))


if __name__ == '__main__':
    conn = RedisClient()
    conn.add(Proxy(host='8.8.8.8', port='888'))
    result = conn.random()
    print(result)
