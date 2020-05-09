from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import time
from selenium.webdriver import ActionChains
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver import ChromeOptions

browser = webdriver.Chrome()


# 初体验
def visit_baidu():
    try:
        browser.get('https://www.baidu.com/')
        input = browser.find_element_by_id('kw')
        input.send_keys('Python')
        input.send_keys(Keys.ENTER)
        wait = WebDriverWait(browser, 10)
        wait.until(EC.presence_of_all_elements_located(
            (By.ID, 'content_left')))
        print(browser.current_url)
        print(browser.get_cookies())
        print(browser.page_source)
    finally:
        browser.close()


# 节点搜索操作
def visit_taobao():
    browser.get('https://www.taobao.com/')

    # 查找单个节点
    input_first = browser.find_element_by_id('q')
    # input_first = browser.find_element(By.ID, 'q')  # 与上面等价
    input_second = browser.find_element_by_css_selector('#q')
    input_third = browser.find_element_by_xpath('//*[@id="q"]')
    print(input_first, input_second, input_third)

    # 查找多个节点
    lis = browser.find_elements_by_css_selector('.service-bd li')
    print(lis)
    browser.close()


# 节点交互操作
def search_taobao():
    browser.get('https://www.taobao.com/')
    input = browser.find_element_by_id('q')
    input.send_keys('iPhone')
    time.sleep(2)
    input.clear()
    time.sleep(3)
    input.send_keys('HUAWEI')
    time.sleep(2)
    button = browser.find_element_by_class_name('btn-search')
    button.click()


# 动作链操作（拖拽）
def runoob_move():
    url = 'https://www.runoob.com/try/try.php?filename=jqueryui-api-droppable'
    browser.get(url)
    # 切换 Frame
    browser.switch_to.frame('iframeResult')
    source = browser.find_element_by_css_selector('#draggable')
    target = browser.find_element_by_css_selector('#droppable')
    actions = ActionChains(browser)
    actions.drag_and_drop(source, target)
    actions.perform()


# 执行 JS
def exeJS_zhihu():
    url = 'https://www.zhihu.com/explore'
    browser.get(url)
    browser.execute_script('window.scrollTo(0, document.body.scrollHeight)')
    browser.execute_script('alert("To Bottom")')


# 获取节点信息
def get_info():
    url = 'https://dynamic2.scrape.cuiqingcai.com/'
    browser.get(url)

    # 获取属性信息
    logo = browser.find_element_by_class_name('logo-image')
    print(logo)
    print(logo.get_attribute('src'))

    # 获取文本
    span = browser.find_element_by_class_name('logo-title')
    print(span.text)

    # 获取 ID、位置、标签名、大小
    print(f'id: {span.id}')
    print(f'location: {span.location}')
    print(f'tag name: {span.tag_name}')
    print(f'size: {span.size}')


# 延时等待
def delay_wait(implicit=True):
    if implicit:
        # 隐式等待
        browser.implicitly_wait(10)
        browser.get('https://dynamic2.scrape.cuiqingcai.com/')
        input = browser.find_element_by_class_name('logo-image')
        # input = browser.find_element_by_class_name('categories')
        print(input)
    else:
        # 显式等待(关于等待条件，有很多，这里只列出来了俩)
        browser.get('https://www.taobao.com/')
        wait = WebDriverWait(browser, 10)
        # 等待出现 id='q' 的节点
        input = wait.until(EC.presence_of_element_located((By.ID, 'q')))
        # 等待按钮变为可点击状态
        button = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '.btn-search')))
        print(input, button)


# 模拟浏览器前进个后退
def forward_and_back():
    browser.get('https://www.baidu.com/')
    browser.get('https://www.taobao.com/')
    browser.get('https://www.python.org/')
    time.sleep(1)
    browser.back()
    time.sleep(1)
    browser.forward()
    time.sleep(1)
    browser.close()


# Cookies 操作
def cookies_handle():
    browser.get('https://www.zhihu.com/explore')
    print(browser.get_cookies())
    browser.add_cookie({
        'name': 'name',
        'domain': 'www.zhihu.com',
        'value': 'germey'
    })
    print(browser.get_cookies())
    browser.delete_all_cookies()
    print(browser.get_cookies())


# 选项卡管理
def tab_handle():
    url = 'https://www.baidu.com'
    browser.get(url)
    browser.execute_script('window.open()')
    print(browser.window_handles)
    browser.switch_to.window(browser.window_handles[1])
    browser.get('https://www.taobao.com')
    time.sleep(1)
    browser.switch_to.window(browser.window_handles[0])
    browser.get('https://python.org')


# 异常处理
def exception_handle():
    try:
        browser.get('https://www.baidu.com')
    except TimeoutException:
        print('Time Out')
    try:
        browser.find_element_by_id('hello')
    except NoSuchElementException:
        print('No Element')
    finally:
        browser.close()


# 反屏蔽
def anti_spider():
    # # 这行代码直接运行后获取不到页面
    # browser.get('https://antispider1.scrape.cuiqingcai.com/')
    option = ChromeOptions()
    option.add_experimental_option('excludeSwitches', ['enable-automation'])
    option.add_experimental_option('useAutomationExtension', False)
    browser = webdriver.Chrome(options=option)
    browser.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
        'source': 'Object.defineProperty(navigator, "webdriver",'
                  ' {get: () => undefined})'
    })  # python 会将圆括号, 中括号 和 花括号 中的行隐式的连接起来 
    browser.get('https://antispider1.scrape.cuiqingcai.com/')


# 无头模式
def head_without():
    option = ChromeOptions()
    option.add_argument('--headless')
    browser = webdriver.Chrome(options=option)
    browser.set_window_size(1366, 768)
    browser.get('https://www.baidu.com')
    browser.get_screenshot_as_file('preview.png')


if __name__ == '__main__':
    # visit_baidu()
    # visit_taobao()
    # search_taobao()
    # runoob_move()
    # exeJS_zhihu()
    # get_info()
    # delay_wait(implicit=False)
    delay_wait()
    # forward_and_back()
    # cookies_handle()
    # tab_handle()
    # exception_handle()
    # anti_spider()
    # head_without()
