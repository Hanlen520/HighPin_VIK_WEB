import os
from bs4 import BeautifulSoup, Tag


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
    error_dict = dict()

    soup = BeautifulSoup(report_content, 'lxml')
    item_list = soup.select('tr')
    for item in item_list:
        if 'class' in item.attrs:
            if item.attrs['class'] == ['passClass']:
                item_dict[item.td.string] = 0
            if item.attrs['class'] == ['errorClass']:
                item_dict[item.td.string] = 1
                # 捕捉带有Error的异常信息,通过兄弟节点获取异常信息 (前方高能预警!!!)
                error_item_dict = dict()
                # 获取当前节点的兄弟节点
                for error_item in item.next_siblings:
                    # 判断元素是不是Tag类型,如果是则进行边界判断,避免打印别的模块的异常信息
                    if isinstance(error_item, Tag):
                        # 在遍历报告时如果样式出现3个中任意1个.则break,代表一条用例中的所有功能项已经遍历完毕
                        if error_item.attrs['class'][0] in ['passClass', 'errorClass', 'failClass']:
                            break
                        # 需要排除class样式为hiddenRow的功能项(hiddenRow代表已经通过的功能项)
                        if error_item.attrs['class'] != ['hiddenRow']:
                            error_item_name = error_item.select('.testcase')[0].text
                            error_item_content = error_item.select('.popup_window pre')[0].text

                            if 'HTTPError: 502 Server Error: Bad Gateway' in error_item_content:
                                error_item_dict[error_item_name] = 1
                            elif 'HTTPError: 404 Client Error: Not Found for url' in error_item_content:
                                error_item_dict[error_item_name] = 2
                            elif 'ReadTimeout: HTTPConnectionPool' in error_item_content:
                                error_item_dict[error_item_name] = 3
                            else:
                                error_item_dict[error_item_name] = 4    # 未知错误

                error_dict[item.td.string] = error_item_dict

            if item.attrs['class'] == ['failClass']:
                item_dict[item.td.string] = 2
    return item_dict, error_dict


if __name__ == '__main__':
    # get_report_item()
    pass

