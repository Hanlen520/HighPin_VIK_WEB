# -*- coding: utf-8 -*-
__author__ = 'Peng.Zhao'

import os
import json
import datetime
import unittest
import HTMLTestRunner
from monitor.HighPin_VIK.RunModeModule import LoadTestCase
from monitor.HighPin_VIK.EngineModule import CreateTestCaseModule
from monitor.HighPin_VIK.EmailNotice import SendEmail
from monitor.HighPin_VIK.WriteReportToDB import handle_model


def run_test():
    """
    :description: 使用xml运行测试
    """
    # 载入测试用例
    total_test_list = LoadTestCase.load_test_case_for_xml()
    # print(json.dumps(total_test_list, ensure_ascii=False))
    # 定义所有文件的TestSuite
    test_suite_for_all_file = unittest.TestSuite()
    for test_file_dict in total_test_list:
        # 定义单个文件的TestSuite
        test_suite_for_single_file = unittest.TestSuite()
        # 遍历每个文件
        for test_key, test_value in test_file_dict.items():
            # 定义每一个文件的的TestSuite
            test_suite_for_file = unittest.TestSuite()
            # 根据文件生成测试用例类
            test_file_class = CreateTestCaseModule.create_test_case_class_for_file((test_key, test_value))
            # 遍历每个类的测试步骤
            for test_file_case in test_value:
                # 取步骤的title当做测试方法名,并将这个测试方法加入到Test_Suite当中
                test_suite_for_file.addTest(test_file_class(test_file_case['title']))
            # 将每个文件的TestSuite加入到单个的TestSuite当中
            test_suite_for_single_file.addTests(test_suite_for_file)
        # 将每个文件的TestSuite加入整个TestSuite当中
        test_suite_for_all_file.addTests(test_suite_for_single_file)

    now_time = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    save_report_path = os.path.join(os.path.abspath('.'), 'monitor', 'static', 'report')
    file_name = save_report_path + '/result_' + now_time + '.html'
    with open(file_name, 'wb') as file_open:
        runner = HTMLTestRunner.HTMLTestRunner(stream=file_open, title='测试结果')
        # 运行测试
        result = runner.run(test_suite_for_all_file)
    # 注意文件路径
    if result is not None:
        # 获取测试的状态参数
        error_count = result.error_count
        failure_count = result.failure_count
        SendEmail.send_report(os.path.join(os.path.abspath('.'), 'monitor', 'HighPin_VIK', 'mail_configure.conf'), error_count, failure_count)
        return True
    else:
        return False

