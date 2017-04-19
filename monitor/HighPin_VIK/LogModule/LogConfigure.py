# -*- coding: utf-8 -*-
__author__ = 'Peng.Zhao'

import os
import logging
import datetime

# 获取当前时间,并且对时间进行格式化
now_time = datetime.datetime.now().strftime('%Y-%m-%d %H-%M-%S')
filename = os.path.abspath('monitor/static/log/') + '/test_log_' + now_time + '.log'
# log的配置信息
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename=filename,
                    filemode='w')

# 创建一个StreamHandler
console = logging.StreamHandler()
# 将INFO级别以上的日志信息打印到控制台
console.setLevel(logging.INFO)
# 设置打印到控制台的日志格式
formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
# 加载格式
console.setFormatter(formatter)
# 添加打印定向,将设置的日志打印到控制台
logging.getLogger('').addHandler(console)

