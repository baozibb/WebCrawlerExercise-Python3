import requests
import logging
import json
import os
import multiprocessing

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s: %(message)s')

INDEX_URL = 'https://dynamic1.scrape.cuiqingcai.com/api/' +\
            'movie/?limit={limit}&offset={offset}'
DETAIL_URL = 'https://dynamic1.scrape.cuiqingcai.com/api/movie/{id}'
LIMIT = 10
TOTAL_PAGE = 10
RESULT_DIR = 'results/Ajax'
os.path.exists(RESULT_DIR) or os.makedirs(RESULT_DIR)

# 运行下面的代码，可以发现获取到的 html 很短，没有想要的内容
# url = 'https://dynamic1.scrape.cuiqingcai.com/'
# html = requests.get(url).text
# print(html)


# 通用的爬取方法
def scrape_api(url):
    logging.info(f'scraping {url} ...')
    try:
        response = requests.get(url)
        if response.status_code == requests.codes.ok:
            return response.json()
        logging.error(f'get invalid status code {response.status_code}\
                        while scraping {url}')
    except requests.RequestException:
        # 将异常异常信息添加到日志消息中
        logging.error(f'error occurred while scraping {url}', exc_info=True)


# 爬取指定页码
def scrape_index(page):
    assert page > 0
    url = INDEX_URL.format(limit=LIMIT, offset=LIMIT*(page-1))
    return scrape_api(url)


# 爬取详情页
def scrape_detail(id):
    url = DETAIL_URL.format(id=id)
    return scrape_api(url)


def main(page):
    index_data = scrape_index(page)  # 爬取列表页
    for item in index_data.get('results'):
        id = item.get('id')
        detail_data = scrape_detail(id)  # 爬取详情页
        logging.info(f'detail data {detail_data}')
        save_data(detail_data)
        logging.info(f'save data {detail_data.get("name")} successfully!!!')


# 保存成 json 文本
def save_data(data):
    name = data.get('name')
    data_path = f"{RESULT_DIR}/{name}.json"
    # ensure_ascii 保证中文字符能正常显示
    # indent=2 表示数据结果有两个空格缩进
    json.dump(data, open(data_path, 'w', encoding='utf-8'),
              ensure_ascii=False, indent=2)


if __name__ == '__main__':
    pool = multiprocessing.Pool()
    pages = range(1, TOTAL_PAGE + 1)
    pool.map(main, pages)
    pool.close()
    pool.join()
