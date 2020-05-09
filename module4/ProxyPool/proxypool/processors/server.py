# -*- coding:utf-8  -*-
# import env
from flask import Flask, g
from proxypool.storages.store_by_redis import RedisClient
from proxypool.setting import API_HOST, API_PORT, API_THREADED

app = Flask(__name__)


def get_conn():
    ''' 获取 redis 客户端对象
   :return: redis 客户端
   '''
    if not hasattr(g, 'redis'):
        g.redis = RedisClient()
    return g.redis


@app.route('/')
def index():
    ''' 获取主界面，可以自定义自己的界面（这里就使用教程的默认界面了）
   :return:
   '''
    return '<h2>Welcome to Proxy Pool System —— by rocketeerli</h2>'


@app.route('/random')
def get_proxy():
    ''' 获取一个随机代理
   :return: 一个随机代理
   '''
    conn = get_conn()
    return conn.random().string()


@app.route('/count')
def get_count():
    ''' 获取代理的数目
   :return: 代理数目
   :rtype: int
   '''
    conn = get_conn()
    return str(conn.count())


if __name__ == '__main__':
    app.run(host=API_HOST, port=API_PORT, threaded=API_THREADED)
