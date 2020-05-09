# -*- coding:utf-8  -*-
class PoolEmptyException(Exception):
    def __str__(self):
        ''' 代理池是空的 '''
        return repr('np proxy in proxypool')
