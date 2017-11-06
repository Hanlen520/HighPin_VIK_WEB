# -*- coding: utf-8 -*-

__author__ = 'Peng.Zhao'

import socket
import requests
import time
import datetime
from monitor.HighPin_VIK.EngineModule import RequestFun
from monitor.HighPin_VIK.VerifyModule import VerifyFun
from monitor.HighPin_VIK.EngineModule import CorraletionRequestParams
from monitor.HighPin_VIK.LogModule import LogConfigure


def test_wrapper_fun(self):
    """
    :description: 测试用例的包装方法
    :return:
    """
    # 每次请求需要存入monitor_request_status表
    resp_status = dict()

    # 使用延迟时间
    if self.wait_seconds_list[self.__class__.index] is not None:
        time.sleep(int(self.wait_seconds_list[self.__class__.index]))
    # 定义接收的变量(避免代码警告提示)
    resp = None
    req_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    # 根据用例中的方法类型选择对应的请求方式,并执行请求
    if self.req_data_list[self.__class__.index]['method'] == 'get':
        resp = RequestFun.test_get_fun(self.req_data_list[self.__class__.index])
    elif self.req_data_list[self.__class__.index]['method'] == 'post':
        resp = RequestFun.test_post_fun(self.req_data_list[self.__class__.index])
    # 不过响应内容不为空,对响应内容进行转码
    resp_content = ''
    if resp is not None:
        resp_content = resp.content.decode('utf-8').strip()

    # 保存入库中的数据
    resp_status['ip'] = self.server_ip
    resp_status['model_name'] = self.case_name
    resp_status['item_name'] = self.title_list[self.__class__.index]
    resp_status['url'] = resp.url
    resp_status['resp_content'] = resp_content
    resp_status['resp_duration'] = resp.elapsed.microseconds / 1000
    resp_status['req_time'] = req_time
    resp_status['status_code'] = resp.status_code
    # 将当前测试用例运行的数据放入monitor_request_status表中
    self.resp_status_list.append(resp_status)

    # 获取当前host中的IP地址
    # ip_address = socket.gethostbyname(resp_status['url'].split('/')[2])
    # LogConfigure.logging.info('IP地址: {}'.format(ip_address))
    if resp.status_code == requests.codes.ok:
        # 显示请求的response(可注释掉)
        # LogConfigure.logging.info(resp_content.replace('\r\n', ''))
        # 加入验证方法
        VerifyFun.verify_function(self, resp_content)
        LogConfigure.logging.info('验证接口: {} --测试通过,返回状态码: {}'.format(self.title_list[self.__class__.index], str(resp.status_code)))
    else:
        resp_content = resp.content.decode('utf-8').strip()
        LogConfigure.logging.info('验证接口: {} --测试失败,返回状态码: {}'.format(self.title_list[self.__class__.index], str(resp.status_code)))
        LogConfigure.logging.info('验证接口: {} --请求返回: {}'.format(self.title_list[self.__class__.index], resp_content))
        resp.raise_for_status()

    # 如果返回值不为None,则执行关联参数的替换操作
    if resp_content is not None:
        CorraletionRequestParams.corr_match(self, resp_content)

    # 利用当前对象配合__class__属性获取当前测试类的静态变量,并进行自加操作
    self.__class__.index += 1

