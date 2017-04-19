# -*- coding: utf-8 -*-

__author__ = 'Peng.Zhao'

import requests
import time
from monitor.HighPin_VIK.EngineModule import RequestFun
from monitor.HighPin_VIK.VerifyModule import VerifyFun
from monitor.HighPin_VIK.EngineModule import CorraletionRequestParams
from monitor.HighPin_VIK.LogModule import LogConfigure


def test_wrapper_fun(self):
    """
    :description: 测试用例的包装方法
    :return:
    """
    # 使用延迟时间
    if self.wait_seconds_list[self.__class__.index] is not None:
        time.sleep(int(self.wait_seconds_list[self.__class__.index]))
    # 定义接收的变量(避免代码警告提示)
    resp = None
    # 根据用例中的方法类型选择对应的请求方式,并执行请求
    if self.req_data_list[self.__class__.index]['method'] == 'get':
        resp = RequestFun.test_get_fun(self.req_data_list[self.__class__.index])
    elif self.req_data_list[self.__class__.index]['method'] == 'post':
        resp = RequestFun.test_post_fun(self.req_data_list[self.__class__.index])

    # 定义接受返回之的变量(避免代码警告提示)
    resp_content = None
    if resp.status_code == requests.codes.ok:
        resp_content = resp.content.decode('utf-8').strip()
        # 显示请求的response(可注释掉)
        # logging.info(resp_content.replace('\r\n', ''))
        # 加入验证方法
        VerifyFun.verify_function(self, resp_content)
        LogConfigure.logging.info('验证接口: ' + self.title_list[self.__class__.index] + '--测试通过,返回状态码: ' + str(resp.status_code))
    else:
        LogConfigure.logging.info('验证接口: ' + self.title_list[self.__class__.index] + '--返回状态码: ' + str(resp.status_code))
        resp.raise_for_status()

    # 如果返回值不为None,则执行关联参数的替换操作
    if resp_content is not None:
        CorraletionRequestParams.corr_match(self, resp_content)

    # 利用当前对象配合__class__属性获取当前测试类的静态变量,并进行自加操作
    self.__class__.index += 1

