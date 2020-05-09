# -*- coding:utf-8  -*-
# 包的引用路径存问题，在这里添加包的地址
# 测试时使用
import sys
import os
BASE_DIR = os.path.dirname(os.path.dirname(
    os.path.abspath(__file__)))  # __file__获取执行文件相对路径，整行为取上一级的上一级目录
BASE_DIR in sys.path or sys.path.append(BASE_DIR)
