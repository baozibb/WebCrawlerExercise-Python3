import requests
import logging
import time
import asyncio
import aiohttp

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s: %(message)s')
TOTAL_NUMBER = 100
BASE_URL = 'https://static4.scrape.cuiqingcai.com/detail/{id}'  # 延迟为 5s 的url


def single_request():
    ''' 单线程 request 爬取 '''
    start_time = time.time()
    for id in range(1, TOTAL_NUMBER + 1):
        url = BASE_URL.format(id=id)
        logging.info(f'scraping {url} ...')
        _ = requests.get(url)
    end_time = time.time()
    logging.info(f'total time {end_time - start_time} seconds')
    # total time 525.3310766220093 secondstotal time 525.3310766220093 seconds


def coroutine_definition():
    ''' 协程的定义 '''
    async def execute(x):
        print('Number: ', x)
    coroutine = execute(1)
    print('Coroutine: ', coroutine)
    print('After calling execute')
    loop = asyncio.get_event_loop()
    loop.run_until_complete(coroutine)
    print('After calling loop')


def coroutine_task():
    ''' 显示地将 coroutine 封装成 task 对象（借助 loop） '''
    async def execute(x):
        print('Number: ', x)
        return x
    coroutine = execute(1)
    print('Coroutine: ', coroutine)
    print('After calling execute')
    loop = asyncio.get_event_loop()
    task = loop.create_task(coroutine)
    print('Task: ', task)
    loop.run_until_complete(task)
    print('Task:', task)
    print('After calling loop')


def coroutine_task_2():
    ''' 显示地将 coroutine 封装成 task 对象（不借助 loop） '''
    async def execute(x):
        print('Number: ', x)
        return x
    coroutine = execute(1)
    print('Coroutine: ', coroutine)
    print('After calling execute')
    task = asyncio.ensure_future(coroutine)
    print('Task: ', task)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(task)
    print('Task: ', task)
    print('After calling loop')


def bind_callback():
    ''' 为 task 绑定回调 '''
    async def request():
        url = 'https://www.baidu.com'
        status = requests.get(url)
        return status

    def callback(task):
        print('Status:', task.result())

    coroutine = request()
    task = asyncio.ensure_future(coroutine)
    task.add_done_callback(callback)
    print('Task: ', task)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(task)
    print('Task: ', task)
    # 不执行回调，直接获得 result
    print('Result: ', task.result())


def multi_task():
    ''' 多任务 asyncio.wait '''
    async def request():
        url = 'https://www.baidu.com'
        status = requests.get(url)
        return status

    tasks = [asyncio.ensure_future(request()) for _ in range(5)]
    print('Task: ', tasks)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.wait(tasks))
    for task in tasks:
        print('Task Result: ', task.result())


def make_coroutine():
    ''' 协程实现 '''
    async def get(url):
        session = aiohttp.ClientSession()
        response = await session.get(url)
        await response.text()
        await session.close()
        return response

    async def request():
        url = 'https://static4.scrape.cuiqingcai.com/'
        print('Waiting for', url)
        response = await get(url)
        print('Get reponse from ', url, ' response: ', response)

    start = time.time()
    tasks = [asyncio.ensure_future(request()) for _ in range(10)]
    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.wait(tasks))
    end = time.time()
    print('Cost time: ', end - start)


def main():
    # single_request()
    # coroutine_definition()
    # coroutine_task()
    # coroutine_task_2()
    # bind_callback()
    # multi_task()
    make_coroutine()


if __name__ == '__main__':
    main()
