# -*- coding:utf-8 -*-
import asyncio
from pyppeteer import launch
from pyppeteer.errors import TimeoutError
import logging
import json
import os

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s: %(message)s')
INDEX_URL = 'https://dynamic2.scrape.cuiqingcai.com/page/{page}'
TIMEOUT = 30
TOTAL_PAGE = 10
WINDOW_WIDTH, WINDOW_HEIGHT = 1366, 768
HEADLESS = True  # 注意，Windows10 系统下，有时候无头模式会加载不出来页面，试了下Ubuntu和Mac，一切正常
browser, tab = None, None

RESULT_DIR = './results/Pyppeteer'
os.path.exists(RESULT_DIR) or os.makedirs(RESULT_DIR)


async def init():
    ''' 初始化浏览器和选项卡，并设置浏览器和选项卡的窗口大小 '''
    global browser, tab
    browser = await launch(headless=HEADLESS,
                           args=[
                               '--disable-infobars',
                               f'--window-size={WINDOW_WIDTH},{WINDOW_HEIGHT}'
                           ])
    tab = await browser.newPage()
    await tab.setViewport({'width': WINDOW_WIDTH, 'height': WINDOW_HEIGHT})


async def scrape_page(url, selector):
    ''' 通用的爬取页面方式 '''
    logging.info('scraping %s', url)
    try:
        await tab.goto(url)
        await tab.waitForSelector(selector,
                                  options={'timeout': TIMEOUT * 1000})
    except TimeoutError:
        logging.error('error occurred while scraping %s', url, exc_info=True)


async def scrape_index(page):
    ''' 爬取列表页 '''
    url = INDEX_URL.format(page=page)
    await scrape_page(url, '.item .name')


async def parse_index():
    ''' 分析列表页，返回 url '''
    # 没太搞懂这个 nodes
    return await tab.querySelectorAllEval(
        '.item .name', 'nodes => nodes.map(node => node.href)')


async def scrape_detail(url):
    ''' 爬取详情页 '''
    await scrape_page(url, 'h2')


async def parse_detail():
    ''' 提取详情页信息 '''
    url = tab.url
    name = await tab.querySelectorEval('h2', 'node => node.innerText')
    categories = await tab.querySelectorAllEval(
        '.categories button span',
        'nodes => nodes.map(node => node.innerText)')
    cover = await tab.querySelectorEval('.cover', 'node => node.src')
    score = await tab.querySelectorEval('.score', 'node => node.innerText')
    drama = await tab.querySelectorEval('.drama p', 'node => node.innerText')
    return {
        'url': url,
        'name': name,
        'categories': categories,
        'cover': cover,
        'score': score,
        'drama': drama
    }


async def save_data(data):
    ''' 保存数据 '''
    name = data.get('name')
    data_path = f'{RESULT_DIR}/{name.replace(":", "")}.json'
    json.dump(data,
              open(data_path, 'w', encoding='utf-8'),
              ensure_ascii=False,
              indent=2)


async def main():
    await init()
    try:
        for page in range(1, TOTAL_PAGE + 1):
            await scrape_index(page)
            detail_urls = await parse_index()
            # logging.info(f'page {page} detail_urls {detail_urls}')
            for detail_url in detail_urls:
                await scrape_detail(detail_url)
                detail_data = await parse_detail()
                movie_name = detail_data.get("name")
                logging.info(f'movie name: {movie_name} detail data: {detail_data}')
                await save_data(detail_data)
                logging.info(f'save movie data {movie_name} successfully')
    finally:
        await browser.close()


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
