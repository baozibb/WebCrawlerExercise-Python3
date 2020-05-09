# -*- coding:utf-8  -*-
from attr import attrs, attr


@attrs
class Proxy(object):
    ''' 代理的模式 '''
    host = attr(type=str, default=None)
    port = attr(type=int, default=None)

    def __str__(self):
        ''' toString 函数 '''
        return f'{self.host}:{self.port}'

    def string(self):
        ''' 转成字符串，打印代理时使用 '''
        return self.__str__()


if __name__ == '__main__':
    proxy = Proxy(host='10.10.8.3', port=8080)
    print('proxy', proxy)
    print('proxy', proxy.string())
