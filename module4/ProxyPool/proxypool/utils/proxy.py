# -*- coding:utf-8  -*-
# import env  # 设置环境变量
from proxypool.schemas.proxy import Proxy
import re


def is_valid_proxy(data):
    '''
    检测数据格式是否符合代理格式
    :param data: 代理数据
    :return: 格式是否正确
    '''
    return re.match('\d+\.\d+\.\d+\.\d+:\d+', data)


def convert_proxy_or_proxies(data):
    '''
    将 list 或 str 类型的代理转成 多个或一个格式正确的代理
    :param data: 代理
    :type data: list or str
    :return: [Proxy] or Proxy
    '''
    if not data:
        return None
    if isinstance(data, list):
        result = []
        for item in data:
            item.strip()
            if not is_valid_proxy(item): continue
            host, port = item.split(':')
            result.append(Proxy(host=host, port=port))
        return result
    if isinstance(data, str) and is_valid_proxy(data.strip()):
        host, port = data.split(':')
        return Proxy(host=host, port=port)


if __name__ == '__main__':
    proxy = '10.12.13.14:11'
    proxies = ['124.158.15.56:568', '158.153.152.17:80']
    print('convert proxy: ', convert_proxy_or_proxies(proxy))
    print('convert proxies: ', convert_proxy_or_proxies(proxies))
