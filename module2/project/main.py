from config import Config
from database import Database
import requests
import logging
import re
from pyquery import PyQuery as pq
from urllib.parse import urljoin
import multiprocessing

# 初始化参数
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s : %(message)s')
db = Database(Config('./config.ini', 'database').section)
options = Config('./config.ini', 'website').section
BASE_URL = options[0][1]
TOTAL_PAGE = int(options[1][1])


# 爬取网站页面
def scrape_page(url):
    logging.info(f'start scraping {url}...')
    try:
        response = requests.get(url)
        if response.status_code == requests.codes.ok:
            return response.text
        logging.error(f'get invalid status code {response.status_code} while scraping {url}')
    except requests.RequestException:
        logging.error(f'erro occurred while scrapin {url}', exc_info=True)  # 将异常信息添加到日志消息中


# 爬取列表页
def scrape_index(page):
    index_url = f'{BASE_URL}/page/{page}'
    return scrape_page(index_url)


# 获取详情页
def scrape_detail(url):
    return scrape_page(url)


# 解析列表页，得到详情页 url
def parse_index(html):
    doc = pq(html)
    links = doc('.el-card .name')  # 查找所有的 el-card 下的 name 标签
    for link in links.items():
        href = link.attr('href')
        detail_url = urljoin(BASE_URL, href)  # 无论 href 是不是短连接，都能拼成绝对路径
        logging.info(f'get detail url f{detail_url}')
        yield detail_url  # 作为一个生成器，每次返回一个详情页的 url


# 解析详情页
def parse_detail(html):
    doc = pq(html)
    cover = doc('img.cover').attr('src')
    name = doc('a > h2').text()  # 这里的 > 选择器表示只选择儿子节点，不选择所有子孙节点
    categories = [item.text() for item in doc('.categories button span').items()]
    published_at = doc('.info:contains(上映)').text()
    published_at = re.search(r'(\d{4}-\d{2}-\d{2})', published_at).group(1) \
        if published_at and re.search(r'\d{4}-\d{2}-\d{2}', published_at) else None
    drama = doc('.drama p').text()  # 获取剧情简介
    score = doc('p.score').text()
    score = float(score) if score else None
    return {
        'cover': cover,  # 封面图链接
        'name': name,  # 电影名
        'categories': categories,  # 分类信息
        'published_at': published_at,  # 上映时间
        'drama': drama,  # 剧情简介
        'score': score  # 豆瓣评分
    }


def main(page):
    index_html = scrape_index(page)  # 爬取第 page 页
    detail_urls = parse_index(index_html)  # 解析第 page 页，并返回一个生成器
    for detail_url in detail_urls:
        detail_html = scrape_detail(detail_url)  # 爬取每一个链接的详情页
        data = parse_detail(detail_html)  # 解析每一个详情页
        logging.info(f'from detail urls get data: {data}')
        # 存到数据库
        logging.info('saving data to mongodb')
        db.save_data(data)
        logging.info('data saved successfully')


if __name__ == '__main__':
    # 多进程
    pool = multiprocessing.Pool()
    pages = range(1, TOTAL_PAGE + 1)
    pool.map(main, pages)
    pool.close()
    pool.join()
