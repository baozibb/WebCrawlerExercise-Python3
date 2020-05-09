# -*- coding:utf-8  -*-
import platform
from os.path import dirname, abspath, join
from environs import Env
from loguru import logger

env = Env()
env.read_env()

# 系统
IS_WINDOWS = platform.system().lower() == 'windows'

# 日志路径
ROOT_DIR = dirname(dirname(abspath(__file__)))  # 项目根目录
LOG_DIR = join(ROOT_DIR, env.str('LOG_DIR', 'logs'))

# 环境  ??? 
DEV_MODE, TEST_MODE, PROD_MODE = 'dev', 'test', 'prod'
APP_ENV = env.str('APP_ENV', DEV_MODE).lower()
APP_DEBUG = env.bool('APP_DEBUG', True if APP_ENV == DEV_MODE else False)
APP_DEV = IS_DEV = APP_ENV == DEV_MODE
APP_PROD = IS_PROD = APP_ENV == PROD_MODE
APP_TEST = IS_TEST = APP_ENV == TEST_MODE

# redis 信息
REDIS_HOST = env.str('REDIS_HOST', '127.0.0.1')
REDIS_PORT = env.int('REDIS_PORT', 6379)
REDIS_PASSWORD = env.str('REDIS_PASSWORD', None)
REDIS_CONNECTION_STRING = env.str('REDIS_CONNECTION_STRING', None)
REDIS_KEY = env.str('REDIS_KEY', 'proxies')
# REDIS_KEY = env.str('REDIS_KEY', 'proxies:universal')

# TODO

# 代理分数
PROXY_SCORE_MAX = 100
PROXY_SCORE_MIN = 0
PROXY_SCORE_INIT = 10
# 代理数目
PROXY_NUMBER_MAX = 50000
PROXY_NUMBER_MIN = 0

# 测试代理的循环时间
CYCLE_TESTER = env.int('CYCLE_TESTER', 20)
# 获取代理的循环时间
CYCLE_GETTER = env.int('CYCLE_GETTER', 100)

# 测试的信息
TEST_URL = env.str('TEST_URL', 'http://www.baidu.com')
TEST_TIMEOUT = env.int('TEST_TIMEOUT', 10)  # 测试的超时时间，默认 10 秒
TEST_BATCH = env.int('TEST_BATCH', 20)  # 异步测试时，每次的 task 数目
TEST_VALID_STATUS = env.list('TEST_VALID_STATUS', [200, 206, 302])  # 测试网站返回的正确状态码

# API 服务接口端参数
API_HOST = env.str('API_HOST', '0.0.0.0')  # 设置 IP 为 0.0.0.0 表示外网可以通过本机 IP 访问，本机访问依然为默认地址
API_PORT = env.int('API_PORT', 5555)
API_THREADED = env.bool('API_THREADED', True)

# enable 设置三个模块是否启动
ENABLE_TESTER = env.bool('ENABLE_TESTER', True)
ENABLE_GETTER = env.bool('ENABLE_GETTER', True)
ENABLE_SERVER = env.bool('ENABLE_SERVER', True)

# 设置日志输出地址、定时创建和最长保留时间
logger.add(env.str('LOG_RUNTIME_FILE', 'runtime.log'), level='DEBUG', rotation='1 week', retention='20 days')
logger.add(env.str('LOG_ERROE_FILE', 'error.log'), level='ERROR', rotation='1 week')
