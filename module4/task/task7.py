# -*- coding:utf-8  -*-
import requests
from urllib.parse import urljoin
from selenium import webdriver
import time


class LoginWithCookies():
    ''' 使用 cookies 的方式进行模拟登陆 '''
    def __init__(self,
                 baseurl='https://login2.scrape.cuiqingcai.com/',
                 username='admin',
                 password='admin'):
        self.baseurl = baseurl
        self.login_url = urljoin(baseurl, '/login')
        self.index_url = urljoin(baseurl, '/page/1')
        self.username = username
        self.password = password

    def login(self):
        session = requests.Session()
        session.post(self.login_url,
                     data={
                         'username': self.username,
                         'password': self.password
                     })
        cookies = session.cookies
        print('Coolies: ', cookies)

        response = session.get(self.index_url)
        print('Response Status: ', response.status_code)
        print('Response URL: ', response.url)


class LoginWithSelenium(LoginWithCookies):
    '''
    为解决复杂登录情况，如验证码、加密参数等
    首先，使用 selenium 进行模拟登陆
    然后把成功登陆后的 cookies 交给 requests 进行页面爬取
    '''
    def login(self):
        browser = webdriver.Chrome()
        browser.get(self.baseurl)
        browser.find_element_by_css_selector(
            'input[name="username"]').send_keys(self.username)
        browser.find_element_by_css_selector(
            'input[name="password"]').send_keys(self.password)
        browser.find_element_by_css_selector('input[type="submit"]').click()
        time.sleep(10)
        # 获取 cookies
        cookies = browser.get_cookies()
        print('Cookies: ', cookies)
        browser.close()
        # 将 cookies 交给 requests
        session = requests.Session()
        for cookie in cookies:
            session.cookies.set(cookie['name'], cookie['value'])
        response = session.get(self.index_url)
        print('Response Status: ', response.status_code)
        print('Response URL: ', response.url)


class LoginWithJWT():
    '''  '''
    def __init__(self,
                 baseurl='https://login3.scrape.cuiqingcai.com/',
                 username='admin',
                 password='admin'):
        self.basurl = baseurl
        self.login_url = urljoin(baseurl, '/api/login')
        self.index_url = urljoin(baseurl, '/api/book')
        self.username = username
        self.password = password

    def login(self):
        response_login = requests.post(self.login_url, json={
            'username': self.username,
            'password': self.password
        })
        data = response_login.json()
        print('Response JSONL: ', data)
        jwt = data.get('token')
        print('JWT: ', jwt)
        headers = {
            'Authorization': f'jwt {jwt}'
        }
        response_index = requests.get(self.index_url, params={
            'limit': 18,
            'offset': 0
        }, headers=headers)
        print('Response Status: ', response_index.status_code)
        print('Response URL: ', response_index.url)
        print('Response Data: ', response_index.json())


if __name__ == '__main__':
    # 使用 cookies + session 进行模拟登陆
    # LoginWithCookies().login()

    # 使用 selenium + requests 进行模拟登陆
    # LoginWithSelenium().login()

    # 使用 requests + JWT 进行模拟登陆
    LoginWithJWT().login()
