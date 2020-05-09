from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import logging
from urllib.parse import urljoin
import os
import json


logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s: %(message)s')
INDEX_URL = 'https://dynamic2.scrape.cuiqingcai.com/page/{page}'
TIME_OUT = 10
TOTAL_PAGE = 10
RESULTS_DIR = 'results/Selenium'

options = webdriver.ChromeOptions()
options.add_argument('--headless')
browser = webdriver.Chrome(options=options)
os.path.exists(RESULTS_DIR) or os.makedirs(RESULTS_DIR)


def scrape_page(url, condition, locator):
    ''' 使用 selenium 进入到 url 页面，并根据条件进行等待 '''
    logging.info(f'scraping {url}')
    wait = WebDriverWait(browser, TIME_OUT)
    try:
        browser.get(url)
        wait.until(condition(locator))  # 根据指定条件等待指定元素
    except TimeoutException:
        logging.error(f'error occurred while scraping {url}', exc_info=True)


def scrape_index(page):
    ''' 进入指定页面的列表页 '''
    url = INDEX_URL.format(page=page)
    # 等待所有列表页的电影元素存在且可见
    scrape_page(url, condition=EC.visibility_of_all_elements_located,
                locator=(By.CSS_SELECTOR, '#index .item'))


def parse_index():
    ''' 解析列表页，返回当前浏览器页面的每一个详情页的 url '''
    # 定位链接
    elements = browser.find_elements_by_css_selector('#index .item .name')
    for element in elements:
        href = element.get_attribute('href')
        yield urljoin(INDEX_URL, href)


def scrape_detail(url):
    ''' 进入到详情页 '''
    # 等待的元素设置成 h2 标签的可见
    scrape_page(url, condition=EC.visibility_of_element_located,
                locator=(By.TAG_NAME, 'h2'))


def parse_detail():
    ''' 分析详情页，获取信息 '''
    url = browser.current_url
    name = browser.find_element_by_tag_name('h2').text
    categories = [element.text for element in
                  browser.find_elements_by_css_selector(
                      '.categories button span')]
    cover = browser.find_element_by_css_selector('.cover').get_attribute('src')
    score = browser.find_element_by_class_name('score').text
    drama = browser.find_element_by_css_selector('.drama p').text
    return {
        'url': url,
        'name': name,
        'categories': categories,
        'cover': cover,
        'score': score,
        'drama': drama
    }


def save_data(data):
    ''' 保存数据到 json 文件中 '''
    name = data.get('name')
    data_path = f'{RESULTS_DIR}/{name.replace(":", "")}.json'
    json.dump(data, open(data_path, 'w', encoding='utf-8'),
              ensure_ascii=False, indent=2)


def main():
    try:
        for page in range(1, TOTAL_PAGE + 1):
            scrape_index(page=page)
            detail_urls = parse_index()
            for detail_url in list(detail_urls):
                logging.info(f'get detail urls {detail_url}')
                scrape_detail(detail_url)
                detail_data = parse_detail()
                logging.info(f'detail data {detail_data}')
                save_data(data=detail_data)
                logging.info(f'data is successfully saved')
    finally:
        browser.close()


if __name__ == '__main__':
    main()
