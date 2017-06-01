import os   #这里很坑--如果从外部调用Django ORM需要设定os.environ()/django.setup()
os.environ['DJANGO_SETTINGS_MODULE'] = 'HighPin_VIK_WEB.settings'

import django   #这里更坑
django.setup()

from monitor.HighPin_VIK.WriteReportToDB.spider_report import get_report_info, get_report_item
from monitor.models import Report, Item, Item_Error


def save_several_report_title():
    # 获取存放报告的路径
    project_path = os.path.abspath('.')
    report_folder_path = os.path.join(project_path, 'monitor', 'static', 'report')
    print(report_folder_path)
    report_list = os.listdir(project_path)
    # 批量导入报告
    for report in report_list:
        last_report_path = os.path.join(project_path, report)
        report_record = get_report_info(last_report_path)

        report = Report.objects.create(**report_record)
        report.save()

        record_date = report_record['create_date']
        save_report_item(report, last_report_path, record_date)


def save_report_title():
    # 获取报告存放路径并获取报告列表
    # project_path = os.path.abspath('.')
    project_path = os.path.abspath('../../../')
    report_folder_path = os.path.join(project_path, 'monitor', 'static', 'report')
    print(report_folder_path)
    report_list = os.listdir(report_folder_path)

    # 对报告列表进行排序
    report_list = sorted(report_list)

    last_report_path = os.path.join(report_folder_path, report_list[-1])
    print(last_report_path)

    # 获取最新的报告信息
    report_record = get_report_info(last_report_path)
    print(report_record)

    # 定义最新报告,并存入DB
    report = Report.objects.create(**report_record)
    report.save()

    # 获取报告日期
    record_date = report_record['create_date']
    # 将报告中的内容保存到Item表
    save_report_item(report, last_report_path, record_date)


def save_report_item(report, last_report_path, record_date):
    item_dict, error_dict = get_report_item(last_report_path)
    for model_name, error_flag in item_dict.items():
        # print(model_name.split('.')[-1], error_flag)
        report_item = {
            'model_name': model_name.split('.')[-1],
            'record_date': record_date,
            'error_flag': error_flag,
            'report_id': report.id  # 外键关联保存
        }

        item = Item.objects.create(**report_item)
        item.save()

        # 保存Error的item
        if model_name in error_dict:
            save_error_item(item, error_dict[model_name], record_date)


def save_error_item(item, error_item_dict, record_date):
    # 保存错误的测试条目,并保存错误类型
    for error_item_key, error_item_value in error_item_dict.items():
        error_item = {
            'model_name': item.model_name,
            'item_name': error_item_key,
            'error_type_flag': error_item_value,
            'record_date': record_date,
            'item_id': item.id
        }

        item_error = Item_Error.objects.create(**error_item)
        item_error.save()

# 写入数据库测试
if __name__ == '__main__':
    save_report_title()
