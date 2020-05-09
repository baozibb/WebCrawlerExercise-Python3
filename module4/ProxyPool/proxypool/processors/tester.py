# -*- coding:utf-8  -*-
# import env  # 设置环境变量
import asyncio
import aiohttp
from loguru import logger
from proxypool.schemas.proxy import Proxy
from proxypool.storages.store_by_redis import RedisClient
from proxypool.setting import TEST_TIMEOUT, TEST_BATCH, TEST_URL, TEST_VALID_STATUS
from aiohttp import ClientProxyConnectionError, ServerDisconnectedError, ClientOSError, ClientHttpProxyError
from asyncio import TimeoutError

EXCEPTIONS = (
    ClientProxyConnectionError, 
    ConnectionRefusedError,
    TimeoutError,
    ServerDisconnectedError,
    ClientOSError,
    ClientHttpProxyError
)


class Tester(object):
    ''' 代理池的 tester, 用于测试在队列中的代理 '''
    def __init__(self):
        ''' 初始化 redis '''
        self.redis = RedisClient()
        self.loop = asyncio.get_event_loop()

    async def test(self, proxy: Proxy):
        ''' 测试一个代理 
        :param proxy: Proxy object
        :return:
        '''
        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
            try:
                logger.debug(f'testing {proxy.string()}')
                async with session.get(TEST_URL, proxy=f'http://{proxy.string()}', timeout=TEST_TIMEOUT,
                                       allow_redirects=False) as response:
                    if response.status in TEST_VALID_STATUS:
                        self.redis.max(proxy)
                        logger.debug(f'proxy {proxy.string()} is valid, set max score')
                    else:
                        self.redis.decrease(proxy)
                        logger.debug(f'proxy {proxy.string()} is invalid, decrease score')
            except EXCEPTIONS:
                self.redis.decrease(proxy)
                logger.debug(f'proxy {proxy.string()} is invalid, decrease score')

    @logger.catch
    def run(self):
        ''' 测试主函数 '''
        logger.info('stating tester...')
        count = self.redis.count()
        logger.debug(f'{count} proxies to test')
        for i in range(0, count, TEST_BATCH):
            start, end = i, min(i + TEST_BATCH, count)
            logger.debug(f'testing proxies from {start} to {end} indices')
            proxies = self.redis.batch(start, end)
            tasks = [self.test(proxy) for proxy in proxies]
            self.loop.run_until_complete(asyncio.wait(tasks))


if __name__ == '__main__':
    tester = Tester()
    tester.run()
