# -*- coding:utf-8  -*-
# import env  # 设置环境变量
import time
import multiprocessing
from proxypool.processors.server import app
from proxypool.processors.getter import Getter
from proxypool.processors.tester import Tester
from proxypool.setting import CYCLE_GETTER, CYCLE_TESTER, API_HOST, API_PORT, API_THREADED,\
     ENABLE_GETTER, ENABLE_TESTER, ENABLE_SERVER, IS_WINDOWS
from loguru import logger

if IS_WINDOWS:
    multiprocessing.freeze_support()

tester_process, getter_process, server_process = None, None, None


class Scheduler():
    ''' 调度器 '''
    def run_tester(self, cycle=CYCLE_TESTER):
        ''' 运行测试模块 tester '''
        if not ENABLE_TESTER:
            logger.info('tester not enabled, exit')
            return
        tester = Tester()
        loop = 0
        while True:
            logger.debug(f'tester loop {loop} start ...')
            tester.run()
            loop += 1
            time.sleep(cycle)

    def run_getter(self, cycle=CYCLE_GETTER):
        ''' 运行获取模块 getter '''
        if not ENABLE_GETTER:
            logger.info(f'getter not enabled, exit')
            return
        getter = Getter()
        loop = 0
        while True:
            logger.debug(f'getter loop {loop} start ...')
            getter.run()
            loop += 1
            time.sleep(cycle)

    def run_server(self):
        ''' 运行接口模块 server '''
        if not ENABLE_SERVER:
            logger.info(f'server not enabled, exit')
            return
        app.run(host=API_HOST, port=API_PORT, threaded=API_THREADED)

    def run(self):
        global tester_process, getter_process, server_process
        try:
            logger.info('starting proxypool...')
            if ENABLE_TESTER:
                tester_process = multiprocessing.Process(target=self.run_tester)
                logger.info(f'starting tester, pid {tester_process.pid}...')
                tester_process.start()
                logger.info(f'starting tester, pid {tester_process.pid}...')

            if ENABLE_GETTER:
                getter_process = multiprocessing.Process(target=self.run_getter)
                logger.info(f'starting getter, pid {getter_process.pid}...')
                getter_process.start()
                logger.info(f'starting getter, pid {getter_process.pid}...')

            if ENABLE_SERVER:
                server_process = multiprocessing.Process(target=self.run_server)
                logger.info(f'starting server, pid {server_process.pid}...')
                server_process.start()
                logger.info(f'starting server, pid {server_process.pid}...')

            if tester_process: tester_process.join()
            if getter_process: getter_process.join()
            if server_process: server_process.join()
        except KeyboardInterrupt:
            logger.info('received keyboard interrupt signal')
            if tester_process: tester_process.terminate()
            if getter_process: getter_process.terminate()
            if server_process: server_process.terminate()
        finally:
            if tester_process:
                tester_process.join()
                logger.info(f'tester is {"alive" if tester_process.is_alive() else "dead"}')
            if getter_process:
                getter_process.join()
                logger.info(f'getter is {"alive" if getter_process.is_alive() else "dead"}')
            if server_process:
                server_process.join()
                logger.info(f'server is {"alive" if server_process.is_alive() else "dead"}')
            logger.info('proxy terminated')


if __name__ == '__main__':
    sch = Scheduler()
    sch.run()
