# -*- coding:utf-8  -*-
import time
from io import BytesIO
from PIL import Image
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from chaojiying import Chaojiying_Client

USERNAME = 'admin'
PASSWORD = 'admin'
CHAOJIYING_USERNAME = 'rocketeerli'
CHAOJIYING_PASSWORD = 'liguojian123.'
CHAOJIYING_SOFT_ID = 905146
CHAOJIYING_KIND = 9004


class CrackCaptcha():
    def __init__(self):
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        self.url = 'https://captcha3.scrape.cuiqingcai.com/'
        self.browser = webdriver.Chrome(options=options)
        self.wait = WebDriverWait(self.browser, 20)
        self.username = USERNAME
        self.password = PASSWORD
        self.chaojiying = Chaojiying_Client(CHAOJIYING_USERNAME, CHAOJIYING_PASSWORD, CHAOJIYING_KIND)

    def open(self):
        ''' 打开网页输入用户名和密码
        :return: None
        '''
        self.browser.get(self.url)
        # 填入用户名和密码
        username = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[type="text"]')))
        password = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[type="password"]')))
        username.send_keys(self.username)
        password.send_keys(self.password)

    def get_captcha_button(self):
        ''' 获取出试验中按钮 '''
        button = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'button[type="button"]')))
        return button

    def get_captcha_element(self):
        ''' 获取验证图像对象 '''
        # 等待验证码图片加载出来
        self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'img.geetest_item_img')))
        # 验证码完整节点
        element = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.geetest_panel_box.geetest_panelshowclick')))
        print('成功获取验证码节点')
        return element

    def get_captcha_position(self):
        ''' 获取验证码位置 '''
        element = self.get_captcha_element()
        time.sleep(2)
        location = element.location
        size = element.size
        print(f'location: {location}, size: {size}')
        top, bottom, left, right = (location['y'], location['y'] + size['height'],
                                    location['x'], location['x'] + size['width'])
        return (top, bottom, left, right)

    def get_screenshot(self, name='screenshoot.png'):
        ''' 获取网页截图 '''
        screenshot = self.browser.get_screenshot_as_png()
        print(f'type: {type(screenshot)}')
        img = BytesIO(screenshot)
        print(f'type: {type(img)}')
        screenshot = Image.open(img)
        print(f'type: {type(screenshot)}')
        screenshot.save(name)
        return screenshot

    def get_captcha_image(self, name='captcha.png'):
        ''' 获取验证码图片 '''
        top, bottom, left, right = self.get_captcha_position()
        print(f'验证码位置: top: {top}, bottom: {bottom}, left: {left}, right: {right}')
        screenshot = self.get_screenshot()
        captcha = screenshot.crop((left, top, right, bottom))
        captcha.save(name)
        return captcha

    def get_points(self, captcha_result):
        ''' 解析超级鹰返回的结果 
        :param captcha_result: 识别结果 形式为 'pic_str': '132,127|56,77'
        :return: 转化后的结果
        '''
        groups = captcha_result.get('pic_str').split('|')
        locations = [[int(number) for number in group.split(',')] for group in groups]
        return locations

    def touch_click_words(self, locations):
        ''' 按照位置点击图片验证码
        :param locations: 识别图像的结果位置
        '''
        for location in locations:
            print('location: ', location)
            ActionChains(self.browser).move_to_element_with_offset(self.get_captcha_element(), location[0], location[1]).click().perform()
            time.sleep(1)

    def touch_click_verify(self):
        ''' 每点击一下，会出现一个小圆圈，判断这个是否存在 '''
        is_clicked = self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'div.geetest_big_mark.geetest_mark_show')))
        print(f'is_clicked: {is_clicked}')

    def login(self):
        ''' 验证成功后，点击确认 '''
        submit = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.geetest_commit_tip')))
        ActionChains(self.browser).move_to_element(submit).click().perform()
        time.sleep(5)
        print('点击确认按钮成功')

    def crack(self):
        ''' 程序入口 '''
        self.open()
        button = self.get_captcha_button()
        button.click()  # 点击登录按钮
        image = self.get_captcha_image()
        # 利用超级鹰
        bytes_array = BytesIO()
        image.save(bytes_array, format='PNG')
        result = self.chaojiying.PostPic(bytes_array.getvalue(), CHAOJIYING_KIND)
        print('result: ', result)
        locations = self.get_points(result)
        self.touch_click_words(locations)
        self.touch_click_verify()
        self.get_screenshot(name='screenshoot_login_before.png')
        self.login()
        # 判定是否成功
        self.get_screenshot(name='screenshoot_login_after.png')
        success = self.wait.until(EC.text_to_be_present_in_element((By.TAG_NAME, 'h2'), '登录成功'))
        print(f'success: {success}')
        print('登录成功') if success else print('登录失败')


if __name__ == '__main__':
    if not CHAOJIYING_USERNAME or not CHAOJIYING_PASSWORD:
        print('请设置用户名或密码')
        exit(0)
    crack_captcha = CrackCaptcha()
    crack_captcha.crack()
