import aiohttp
import asyncio


async def basic_eg():
    ''' 基本案例 '''
    async def fetch(session, url):
        ''' 使用 session 爬取 url '''
        # 声明一个支持异步的上下文管理器
        async with session.get(url) as response:
            # 返回的 coroutine 对象前面需要添加 await 来修饰
            return await response.text(), response.status

    async with aiohttp.ClientSession() as session:
        url = 'https://cuiqingcai.com'
        html, status = await fetch(session, url)
        print(f'html: {html[:100]} ...')
        print(f'status: {status}')


async def url_params():
    ''' url 参数设置 '''
    params = {'name': 'rocketeerli', 'age': 23}
    # get 请求
    async with aiohttp.ClientSession() as session:
        url = 'https://httpbin.org/get'
        async with session.get(url, params=params) as response:
            print(await response.text())
    # post 请求
    async with aiohttp.ClientSession() as session:
        url = 'https://httpbin.org/post'
        # form 格式
        async with session.post(url, data=params) as response:
            print(await response.text())
        # json 格式
        async with session.post(url, json=params) as response:
            print(await response.text())


async def get_response():
    ''' 获取响应字段 '''
    data = {'name': 'rocketeerli', 'age': 23}
    async with aiohttp.ClientSession() as session:
        url = 'https://httpbin.org/post'
        async with session.post(url, data=data) as response:
            print('status: ', response.status)
            print('headers: ', response.headers)
            print('body: ', await response.text())
            print('bytes: ', await response.read())
            print('json: ', await response.json())


async def timeout_setting():
    ''' 超时设置 '''
    timeout = aiohttp.ClientTimeout(total=10)
    async with aiohttp.ClientSession(timeout=timeout) as session:
        url = 'https://httpbin.org/get'
        async with session.get(url) as response:
            print('status: ', response.status)


async def concurrency_handle():
    ''' 并发控制 '''
    concurrency = 5
    url = 'https://www.baidu.com'
    semaphore = asyncio.Semaphore(concurrency)
    session = aiohttp.ClientSession()

    async def scrape_api():
        async with semaphore:
            print('scraping ', url)
            async with session.get(url) as response:
                await asyncio.sleep(1)
                return await response.text()

    scrape_index_tasks = [asyncio.ensure_future(scrape_api())
                          for _ in range(10000)]
    await asyncio.gather(*scrape_index_tasks)


def main():
    loop = asyncio.get_event_loop()
    # loop.run_until_complete(basic_eg())
    # loop.run_until_complete(url_params())
    # loop.run_until_complete(get_response())
    # loop.run_until_complete(timeout_setting())
    loop.run_until_complete(concurrency_handle())


if __name__ == '__main__':
    main()
