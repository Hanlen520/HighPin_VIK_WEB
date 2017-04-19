import os
from bs4 import BeautifulSoup


def get_report_info(last_report_path):
    with open(last_report_path, encoding='UTF-8') as f:
        report_content = f.read()

    soup = BeautifulSoup(report_content, 'lxml')
    report_create_time = soup.select('div.heading > p.attribute')

    report_create_time_str_array = report_create_time[0].text.split(' ')
    create_time = report_create_time_str_array[-1]
    create_date = report_create_time_str_array[-2]

    print(create_date, create_time)

    report_status_str_array = report_create_time[2].text.split(' ')
    failure_num = 0
    error_num = 0
    if 'Failure' in report_status_str_array:
        failure_num = report_status_str_array.index('Failure')
    if 'Error' in report_status_str_array:
        error_num = report_status_str_array.index('Error')

    if failure_num + error_num > 0:
        is_error = True
    else:
        is_error = False

    report_name = last_report_path.split(os.sep)[-1]
    report_record = {
        'report_name': report_name,
        'create_date': create_date,
        'create_time': create_time,
        'is_error': is_error
    }
    return report_record


def get_report_item(last_report_path):
    with open(last_report_path, encoding='UTF-8') as f:
        report_content = f.read()

    item_dict = dict()

    soup = BeautifulSoup(report_content, 'lxml')
    item_list = soup.select('tr')
    for item in item_list:
        if 'class' in item.attrs:
            if item.attrs['class'] == ['passClass']:
                # print(item.td.string)
                item_dict[item.td.string] = 0
            if item.attrs['class'] == ['errorClass']:
                # print(item.td.string)
                item_dict[item.td.string] = 1
            if item.attrs['class'] == ['failClass']:
                # print(item.td.string)
                item_dict[item.td.string] = 2
    return item_dict


if __name__ == '__main__':
    # get_report_item()
    pass

