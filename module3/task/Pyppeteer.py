import asyncio
from pyppeteer import launch
from pyquery import PyQuery as pq

'''
pyppeteer API 网址
https://miyakogi.github.io/pyppeteer/reference.html
'''
width, height = 1366, 768


async def use_browser():
    ''' 使用 pyppeteer 中的浏览器 '''
    browser = await launch()
    page = await browser.newPage()
    await page.goto('https://dynamic2.scrape.cuiqingcai.com/')
    await page.waitForSelector('.item .name')
    doc = pq(await page.content())
    names = [item.text() for item in doc('.item .name').items()]
    print('Names: ', names)
    await browser.close()


async def execute_js():
    ''' 执行 js 语句，并截图 '''
    browser = await launch()
    page = await browser.newPage()
    await page.setViewport({'width': width, 'height': height})
    await page.goto('https://dynamic2.scrape.cuiqingcai.com/')
    await page.waitForSelector('.item .name')
    await asyncio.sleep(2)
    await page.screenshot(path='example.png')
    dimensions = await page.evaluate('''() => {
        return {
            width: document.documentElement.clientWidth,
            height: document.documentElement.clientHeight,
            deviceScaleFactor: window.devicePixelRatio,
        }
    }''')
    print(dimensions)
    await browser.close()

class Args_launch():
    ''' launch 方法的一些参数 '''
    async def headless(self):
        ''' 体验参数——无头模式 '''
        browser = await launch(headless=False)
        await asyncio.sleep(100)
        await browser.close()

    async def devtools(self):
        ''' 体验参数——调试模式 '''
        # devtools = True 时，headless 参数无效
        browser = await launch(devtools=True)
        page = await browser.newPage()
        await page.goto('https://www.baidu.com/')
        await asyncio.sleep(10)
        await browser.close()

    async def disable_info(self):
        ''' 禁用提示条（如：Chrome 正受到自动测试软件的控制） '''
        browser = await launch(devtools=True, args=['--disable-infobars'])
        page = await browser.newPage()
        await page.goto('https://taobao.com/')
        # 会检测到是 WebDriver
        # await page.goto('https://antispider1.scrape.cuiqingcai.com/')
        await asyncio.sleep(30)
        await browser.close()

    async def executeJS_hiddenWebDriver(self):
        ''' 使用执行 js 语句的方法，隐藏 WebDriver '''
        # 设置浏览器宽高
        browser = await launch(headless=False, args=['--disable-infobars', f'--window-size={width},{height}'])
        page = await browser.newPage()
        # 设置页面显示的宽高
        await page.setViewport({'width': width, 'height': height})
        await page.evaluateOnNewDocument('Object.defineProperty(navigator,'
                                         '"webdriver", {get:() => undefined})')
        await page.goto('https://antispider1.scrape.cuiqingcai.com/')
        await asyncio.sleep(30)
        await browser.close()

    async def data_persistence(self):
        ''' 设置用户目录，保存登录状态，用于数据持久化 '''
        browser = await launch(headless=False, userDataDir='./userdata',
                               args=['--disable-infobars'])
        page = await browser.newPage()
        await page.goto('https://www.taobao.com/')
        await asyncio.sleep(60)
        await browser.close()


class Method_browser:
    ''' 浏览器的一些方法 '''
    def __init__(self, width=1200, height=768):
        self.width = width
        self.height = height

    async def incognito_model(self):
        ''' 无痕模式 '''
        browser = await launch(headless=False, args=['--disable-infobars',
                               f'--window-size={self.width},{self.height}'])
        context = await browser.createIncognitoBrowserContext()
        page = await context.newPage()
        await page.setViewport({'width': self.width, 'height': self.height})
        await page.goto('https://www.baidu.com/')
        await asyncio.sleep(60)
        await browser.close()

class Method_page():
    ''' 页面的一些方法 '''
    def __init__(self):
        pass

    async def selector(self):
        ''' page 的选择器方法 '''
        browser = await launch()
        page = await browser.newPage()
        await page.goto('https://dynamic2.scrape.cuiqingcai.com/')
        await page.waitForSelector('.item .name')
        j_result1 = await page.J('.item .name')
        j_result2 = await page.querySelector('.item .name')
        jj_result1 = await page.JJ('.item .name')
        jj_result2 = await page.querySelectorAll('.item .name')
        print('J Result:', j_result1)
        print('J Result2:', j_result2)
        print('JJ Result1:', jj_result1)
        print('JJ Result2:', jj_result2)
        await browser.close()

    async def tab(self):
        ''' 选项卡操作 '''
        browser = await launch(headless=False)
        page = await browser.newPage()
        await page.goto('https://www.baidu.com/')
        page = await browser.newPage()
        await page.goto('https://www.bing.com')
        pages = await browser.pages()
        print('Pages: ', pages)
        page1 = pages[1]
        await page1.bringToFront()
        await asyncio.sleep(10)

    async def normal(self):
        ''' 常规操作 '''
        browser = await launch(headless=False)
        page = await browser.newPage()
        await page.goto('https://www.baidu.com/')
        await page.goto('https://taobao.com/')
        # 后退
        await page.goBack()
        # 前进
        await page.goForward()
        # 刷新
        await page.reload()
        # # 保存 pdf
        # await page.pdf()  # 出了点问题
        # 截图
        await page.screenshot()
        # 设置页面 HTML
        await page.setContent('<h2>Hello Stranger</h2>')
        # 设置 User-Agent
        await page.setUserAgent('Python')
        # 设置 Headers
        await page.setExtraHTTPHeaders(headers={})
        # 关闭
        await page.close()
        await browser.close()

    async def click(self):
        ''' 点击操作 '''
        browser = await launch(headless=False)
        page = await browser.newPage()
        await page.goto('https://dynamic2.scrape.cuiqingcai.com/')
        await page.waitForSelector('.item .name')
        await page.click('.item .name', options={
            'button': 'right',
            'clickCount': 1,  # 1 or 2
            'delay': 3000  # 毫秒 ms
        })
        await asyncio.sleep(10)
        await browser.close()

    async def input(self):
        ''' 输入文本 '''
        browser = await launch(headless=False)
        page = await browser.newPage()
        await page.goto('https://www.taobao.com/')
        # 前进
        await page.type('#q', 'iPad')  # 第一个参数是选择器，第二个是输入的内容
        await asyncio.sleep(10)
        # 关闭
        await asyncio.sleep(10)
        await browser.close()

    async def get_message(self):
        ''' 获取信息 '''
        browser = await launch(headless=False)
        page = await browser.newPage()
        await page.goto('https://dynamic2.scrape.cuiqingcai.com/')
        print('HTML:', await page.content())
        print('Cookies:', await page.cookies())
        await asyncio.sleep(3)
        await browser.close()

    # 省略执行 js 代码 和 延时等待 waitForSelector 。。见第一个函数


def main():
    loop = asyncio.get_event_loop()
    # loop.run_until_complete(use_browser())
    # loop.run_until_complete(execute_js())
    args_launch = Args_launch()
    # loop.run_until_complete(args_launch.headless())
    # loop.run_until_complete(args_launch.devtools())
    # loop.run_until_complete(args_launch.disable_info())
    # loop.run_until_complete(args_launch.executeJS_hiddenWebDriver())
    # loop.run_until_complete(args_launch.data_persistence())
    method_browser = Method_browser()
    # loop.run_until_complete(method_browser.incognito_model())
    method_page = Method_page()
    # loop.run_until_complete(method_page.selector())
    # loop.run_until_complete(method_page.tab())
    # loop.run_until_complete(method_page.normal())
    # loop.run_until_complete(method_page.click())
    # loop.run_until_complete(method_page.input())
    loop.run_until_complete(method_page.get_message())


if __name__ == '__main__':
    main()
