# -*- coding: utf-8 -*-
__author__ = 'Peng.Zhao'

import unittest
from monitor.HighPin_VIK.EngineModule import PackingTestCase
from monitor.HighPin_VIK.EngineModule import TestFunWrapper


def create_test_case_class(test_module):
    """
    :description: 创建测试用例类
    :param test_module: 测试用例的数据对象
    :return: 单个测试类
    """
    # 载入参数,根据测试用例中的item,分别获取4个列表
    title_list, req_data_list, corr_list, verify_list = PackingTestCase.packing_test_case(test_module.test_case_list)
    # 创建方法字典
    test_member_dict = dict()
    test_member_dict['title_list'] = title_list
    test_member_dict['req_data_list'] = req_data_list
    test_member_dict['corr_list'] = corr_list
    test_member_dict['verify_list'] = verify_list
    # 定义测试类的静态变量,用于流程型用例数据的读取
    test_member_dict['index'] = 0
    # 加入测试方法
    for test_case_title in title_list:
        test_member_dict[test_case_title] = TestFunWrapper.test_wrapper_fun

    # 获取类名
    class_name = test_module.__name__
    # 因为获取的类全名是用"."分割,所以只需要最后的名字即可--name_list[2]
    name_list = class_name.split('.')

    # 创建测试类
    single_test_class = type(name_list[1], (unittest.TestCase,), test_member_dict)
    # single_test_class = type(name_list[2], (unittest.TestCase,), test_member_dict)
    return single_test_class


def create_test_case_class_for_file(test_tuple):
    """
    :description: 创建测试用例类(兼容XML/Excel)
    :param test_tuple: 获取单个测试数据文件的名称和数据
    :return: 返回测试类
    """
    # 载入参数,根据测试用例中的item,分别获取4个列表
    title_list, req_data_list, corr_list, wait_seconds_list, verify_list = PackingTestCase.packing_test_case(test_tuple[1])
    # 创建方法字典
    test_member_dict = dict()
    test_member_dict['title_list'] = title_list
    test_member_dict['req_data_list'] = req_data_list
    test_member_dict['corr_list'] = corr_list
    test_member_dict['wait_seconds_list'] = wait_seconds_list
    test_member_dict['verify_list'] = verify_list
    # 定义测试类的静态变量,用于流程型用例数据的读取
    test_member_dict['index'] = 0
    # 加入测试方法
    for test_case_title in title_list:
        test_member_dict[test_case_title] = TestFunWrapper.test_wrapper_fun

    # 获取类名
    class_name = test_tuple[0]

    # 创建测试类
    single_test_class = type(class_name, (unittest.TestCase,), test_member_dict)
    # single_test_class = type(name_list[2], (unittest.TestCase,), test_member_dict)
    return single_test_class
