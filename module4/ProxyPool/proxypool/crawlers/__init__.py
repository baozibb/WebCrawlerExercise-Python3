# -*- coding:utf-8  -*-
import pkgutil
from .base import BaseCrawler  # 显式本地导入包，不能在主脚本文件中运行
import inspect
'''
    导入该包时会运行 __init__.py 文件
    该文件表示，外部文件使用 from * import * 导入包时，只能导入 BaseCrawler 的子类
'''


# 加载 BaseCrawler 的子类
classes = []
for loader, name, is_pkg in pkgutil.walk_packages(__path__):
    # 根据模块名获得模块的地址，并加载对应的 module
    module = loader.find_module(name).load_module(name)
    for name, value in inspect.getmembers(module):
        # TODO globals()[name] = value
        if inspect.isclass(value) and issubclass(
                value, BaseCrawler) and value is not BaseCrawler:
            classes.append(value)
# 限制 from * import * 中import的包名
__all__ = __ALL__ = classes
# print(__ALL__)
