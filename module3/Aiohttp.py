import asyncio
import aiohttp
import logging
import json
from motor.motor_asyncio import AsyncIOMotorClient

INDEX_URL = ('https://dynamic5.scrape.cuiqingcai.com/api/book/?limit={limit}'
             '&offset={offset}')
DETAIL_URL = 'https://dynamic5.scrape.cuiqingcai.com/api/book/{id}/'
PAGE_SIZE = 18  # 每页展示数
PAGE_NUMBER = 100  # 总页数
CONCURRENCY = 5  # 并发数量

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s: %(message)s')
session = aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=1000))

# 保存数据的配置
MONGO_CONNECTION = 'mongodb://localhost:27017'
MONGO_DB_NAME = 'books'
MONGO_COLLECTION_NAME = 'books'
client = AsyncIOMotorClient(MONGO_CONNECTION)
db = client[MONGO_DB_NAME]
collection = db[MONGO_COLLECTION_NAME]


async def scrape_api(url):
    ''' 通用的爬取方法 '''
    async with asyncio.Semaphore(CONCURRENCY):
        try:
            logging.info('scraping %s', url)
            async with session.get(url, timeout=1600) as response:
                if response.headers.get('content-type').strip() == 'application/json':
                    return await response.json()
                else:
                    logging.info(f'unable to request {url}', exc_info=True)
                    return None
        except aiohttp.ClientError:
            logging.error(f'error occurred while sraping {url}', exc_info=True)


async def scrape_index(page):
    ''' 列表页爬取 '''
    url = INDEX_URL.format(limit=PAGE_SIZE, offset=PAGE_SIZE * (page - 1))
    return await scrape_api(url)


async def scrape_detail(id):
    ''' 详情页爬取 '''
    url = DETAIL_URL.format(id=id)
    data = await scrape_api(url)
    if data:
        await save_data(data)


async def save_data(data):
    ''' 保存数据到 mongodb 数据库中 '''
    logging.info('saving data %s', data)
    if data:
        return await collection.update_one({
            'id': data.get('id')
        }, {
            '$set': data
        }, upsert=True)


async def main_1():
    ''' 将定义的方法串联起来 '''
    scrape_index_tasks = [asyncio.ensure_future(scrape_index(page)) for page in range(1, PAGE_NUMBER + 1)]
    results = await asyncio.gather(*scrape_index_tasks)
    # detail tasks
    print('results', results)
    ids = []
    for index_data in results:
        if not index_data:
            continue
        for item in index_data.get('results'):
            ids.append(item.get('id'))
    scrape_detail_tasks = [asyncio.ensure_future(scrape_detail(id)) for id in ids]
    await asyncio.wait(scrape_detail_tasks)
    await session.close()


async def main_2():
    ''' 将定义的方法串联起来 '''
    for page in range(1, PAGE_NUMBER + 1):
        index_task = scrape_index(page)
        results = await asyncio.gather(index_task)
        logging.info('index data %s', json.dumps(results, ensure_ascii=False, indent=2))
        if not results[0]:
            continue
        ids = []
        for item in results[0].get('results'):
            if not item:
                continue
            ids.append(item.get('id'))
        detail_tasks = [scrape_detail(id) for id in ids]
        await asyncio.gather(*detail_tasks)
    await session.close()


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main_1())
    # loop.run_until_complete(main_2())
