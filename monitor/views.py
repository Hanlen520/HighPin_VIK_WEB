import json
import os
import time

from datetime import datetime, timedelta
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, redirect
from apscheduler.schedulers.background import BackgroundScheduler

from monitor.models import Report, Item, Case
from monitor.HighPin_VIK import VIKRunner
from monitor.HighPin_VIK.GetNewCookie import GetUserCookie
from monitor.HighPin_VIK.WriteReportToDB import handle_model

# 任务计划对象-全局变量(真不想定义这个全局变量)
test_run_schedule = None
refresh_cookie_run_schedule = None


def index(request):
    report_name = request.GET.get('report_name')
    if report_name is None:
        report_name = Report.objects.first()
        if report_name is None:
            return render(request, template_name='index.html')
    return render(request, template_name='index.html', context={'report_name': report_name})


def report_filter(report_from_db, report_id, create_date, is_error):
    if is_error == '':
        # 如果'是否出错'字段为空则只是用前面两个条件进行搜索
        if report_id is '' and create_date is '':
            report_from_db = Report.objects.filter()
        elif report_id is not '' and create_date is '':
            report_from_db = Report.objects.filter(id=report_id)
        elif report_id is '' and create_date is not '':
            report_from_db = Report.objects.filter(create_date=create_date)
        elif report_id is not '' and create_date is not '':
            report_from_db = Report.objects.filter(id=report_id, create_date=create_date)
    else:
        # 如果'是否出错'字段不为空,则使用全部条件进行搜索
        if report_id is '' and create_date is '':
            report_from_db = Report.objects.filter(is_error=is_error)
        elif report_id is not '' and create_date is '':
            report_from_db = Report.objects.filter(id=report_id, is_error=is_error)
        elif report_id is '' and create_date is not '':
            report_from_db = Report.objects.filter(create_date=create_date, is_error=is_error)
        elif report_id is not '' and create_date is not '':
            report_from_db = Report.objects.filter(id=report_id, create_date=create_date, is_error=is_error)
    return report_from_db


def reports_list(request):
    page_no = request.GET.get('page_no')
    report_id = request.POST.get('report_id')
    create_date = request.POST.get('create_date')
    is_error = request.POST.get('is_error')

    # 默认获得第一页的数据
    if page_no is None:
        page_no = 1
    # 如果得到None字符串,需要检查get方式下是否能获取参数
    if report_id is None:
        report_id = request.GET.get('report_id')
        # 如果get方式下获取的是None,用空字符串代替
        if report_id is None:
            report_id = ''
    if create_date is None:
        create_date = request.GET.get('create_date')
        if create_date is None:
            create_date = ''
    if is_error is None:
        is_error = request.GET.get('is_error')
        if is_error is None:
            is_error = ''

    report_from_db = None
    # 根据'是否出错'分成三种情况调用方法
    if is_error == 'true':
        report_from_db = report_filter(report_from_db, report_id, create_date, True)
    elif is_error == 'false':
        report_from_db = report_filter(report_from_db, report_id, create_date, False)
    elif is_error == '' or is_error is None:
        report_from_db = report_filter(report_from_db, report_id, create_date, '')

    # 分页(每一页显示多少报告)
    paginator = Paginator(report_from_db, 15)
    # 获取总共多少页
    num_pages = paginator.num_pages

    try:
        report_list = paginator.page(page_no)
    except PageNotAnInteger:
        # 如果页码不是整型数字
        report_list = paginator.page(1)
    except EmptyPage:
        # 如果页码超出了记录范围,则返回最后一页
        report_list = paginator.page(paginator.num_pages)

    return render(request, template_name='reports_list.html', context={
        'report_list': report_list,
        'page_no': page_no,
        'num_pages': num_pages,
        # 搜索条件
        'report_id': report_id,
        'create_date': create_date,
        'is_error': is_error
    })


def get_new_report_items(request):
    new_report = Report.objects.first()
    new_report_date = None
    new_report_items = None
    if new_report is not None:
        new_report_date = new_report.create_date
        # 按照最新的一天的报告查询(使用extra方法按照model_name排序)
        new_report_items = Item.objects.filter(report_id=new_report.id).extra(order_by=['model_name'])

    return render(request, template_name='items_list.html', context={
        'new_report_items': new_report_items,
        'new_report_date': new_report_date,
    })


def display_chart(request):
    model_name = request.GET.get('model_name')
    end_record_date = request.GET.get('record_date')
    # 字符串转日期
    end_date = datetime.strptime(end_record_date, '%Y-%m-%d').date()
    # 日期减法,获取7天前日期
    begin_date = end_date - timedelta(days=6)
    # 根据起止时间和业务流程名称获取数据(范围查询:xxxx_range=[x,x])
    filter_items = Item.objects.filter(record_date__range=[begin_date, end_date]).filter(model_name=model_name)

    day_list = list()
    day_str_list = list()
    for day in range((end_date - begin_date).days + 1):
        day = begin_date + timedelta(days=day)
        day_list.append(day)   # 需要将日期类型转成字符串
        day_str_list.append(day.strftime('%Y-%m-%d'))

    print(day_list)

    # for q in filter_items:
    #     print(q.id, q.model_name, q.error_flag, q.record_date)

    pass_num = 0
    error_num = 0
    fail_num = 0

    pass_list = list()
    error_list = list()
    fail_list = list()

    # 根据一周7天生成对应状态的列表
    for day in day_list:
        for q in filter_items:
            if day == q.record_date:
                if q.error_flag == 0:
                    pass_num += 1
                if q.error_flag == 1:
                    error_num += 1
                if q.error_flag == 2:
                    fail_num += 1
        pass_list.append(pass_num)
        error_list.append(error_num)
        fail_list.append(fail_num)

        pass_num = 0
        error_num = 0
        fail_num = 0

    # print(pass_list)
    # print(error_list)
    # print(fail_list)

    return render(request, template_name='chart.html', context={
        'model_name': model_name,
        'day_str_list': day_str_list,
        'pass_list': pass_list,
        'error_list': error_list,
        'fail_list': fail_list
    })


def cases_list(request):
    page_no = request.GET.get('page_no')
    case_name = request.POST.get('case_name')

    # 默认获得第一页的数据
    if page_no is None:
        page_no = 1

    # 如果Post提交的表单数据中case_name的值为None,则检查Get提交的case_name
    if case_name is None:
        case_name = request.GET.get('case_name')
        # 如果Get提交的case_name依然为None,则将case_name置为''
        if case_name is None:
            case_name = ''

    if case_name != '' and case_name is not None:
        # 使用__contains进行模糊搜索
        case_from_db = Case.objects.filter(case_name__contains=case_name)
    else:
        case_from_db = Case.objects.filter()

    # 分页(每一页显示多少用例)
    paginator = Paginator(case_from_db, 10)
    # 获取总共多少页
    num_pages = paginator.num_pages

    try:
        case_list = paginator.page(page_no)
    except PageNotAnInteger:
        # 如果页码不是整型数字
        case_list = paginator.page(1)
    except EmptyPage:
        # 如果页码超出了记录范围,则返回最后一页
        case_list = paginator.page(paginator.num_pages)

    return render(request, template_name='cases_list.html', context={
        'case_list': case_list,
        'page_no': page_no,
        'num_pages': num_pages,
        # 搜索条件
        'case_name': case_name
    })


def upload_case(request):
    upload_case_file = request.FILES.get('upload_case')

    # 利用绝对路径确定保存位置
    with open(os.path.dirname(__file__) + '/static/testcase/' + upload_case_file.name, 'wb+') as destination:
        for chunk in upload_case_file.chunks():
            destination.write(chunk)
    # 获取上传时间
    # case_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    case_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    case_record = {'case_name': upload_case_file.name, 'case_time': case_time}
    # 将报告写入到数据库
    case = Case.objects.create(**case_record)
    case.save()
    # 页面重定向
    return redirect('/monitor/cases_list/')


def delete_case(request):
    case_id = request.GET.get('case_id')
    # 根据ID查找用例
    del_case = Case.objects.get(id=case_id)

    test_case_folder_path = os.path.join(os.path.dirname(__file__), 'static', 'testcase')
    test_case_list = os.listdir(test_case_folder_path)

    del_flag = None
    for test_case in test_case_list:
        # 如果在testcase文件夹中能找到这个文件,则进行删除操作
        if del_case.case_name == test_case:
            os.remove(os.path.join(test_case_folder_path, test_case))
            # 删除数据库中的记录
            del_flag = del_case.delete()
    # 显示删除标志位
    # print(del_flag[0])

    return redirect('/monitor/cases_list/')


def test_operate(request):
    return render(request, template_name='test_operate.html', context={})


def run_test(request):
    VIKRunner.run_test()    # 运行测试
    handle_model.save_report_title()    # 将测试报告的内容保存到DB
    return render(request, template_name='test_operate.html', context={})


class SingletonDecorator:
    """
    单例模式装饰类
    """
    def __init__(self, parameter):
        self.parameter = parameter
        self.instance = None

    def __call__(self, *args, **kwargs):
        if self.instance is None:
            self.instance = self.parameter(*args, **kwargs)
        return self.instance


class RefreshCookieScheduleTask:
    """
    声明测试运行的任务计划类
    """
    refresh_cookie_schedule = BackgroundScheduler()

refresh_cookie_scheduler_obj = SingletonDecorator(RefreshCookieScheduleTask)


def refresh_cookie(request):
    """
    更新Cookie的计划任务
    :param request:
    :return:
    """
    cron_list = None
    task_flag = json.loads(request.body.decode())
    if 'run_cron' in task_flag:
        cron_str = task_flag['run_cron'].strip()
        if cron_str != '':
            cron_list = cron_str.split(' ')
        else:
            cron_list = ['*', '10', '0', '*', '*', '*']
    global refresh_cookie_run_schedule  # 使用全局变量
    if refresh_cookie_run_schedule is None:
        if task_flag['run_flag'] == 'start_run':
            refresh_cookie_run_schedule = refresh_cookie_scheduler_obj().refresh_cookie_schedule
            refresh_cookie_run_schedule.add_job(
                task_run_refresh_cookie,        # 任务方法
                trigger='cron',
                second=cron_list[0],
                minute=cron_list[1],
                hour=cron_list[2],
                day=cron_list[3],
                week=cron_list[4],
                month=cron_list[5],
                id='schedule_refresh_cookie'
            )
            refresh_cookie_run_schedule.start()
    else:
        # 如果计划任务已经启动,有两个分支.
        # 1.修改当前任务的执行周期
        # 2.停止当前任务
        if task_flag['run_flag'] == 'start_run':
            refresh_cookie_run_schedule.resume()        # 计划任务恢复-对应任务暂停
            refresh_cookie_run_schedule.reschedule_job(
                job_id='schedule_refresh_cookie',
                trigger='cron',
                second=cron_list[0],
                minute=cron_list[1],
                hour=cron_list[2],
                day=cron_list[3],
                week=cron_list[4],
                month=cron_list[5]
            )
        elif task_flag['run_flag'] == 'stop_run':
            refresh_cookie_run_schedule.pause()         # 计划任务暂停

    return render(request, template_name='test_operate.html', context={})


class TestScheduleTask:
    """
    声明测试运行的任务计划类
    """
    test_schedule = BackgroundScheduler()

test_scheduler_obj = SingletonDecorator(TestScheduleTask)


def timing_task(request):
    """
    执行测试的计划任务
    :param request:
    :return:
    """
    cron_list = None
    # Ajax传过来的json是二进制字符串,需要用decode()转成字符串
    task_flag = json.loads(request.body.decode())
    if 'run_cron' in task_flag:
        cron_str = task_flag['run_cron'].strip()
        if cron_str != '':
            cron_list = cron_str.split(' ')
        else:
            # 如果为空则默认以每隔20分钟运行一次的规则运行
            cron_list = ['*', '*/20', '*', '*', '*', '*']
    global test_run_schedule     # 使用全局变量
    if test_run_schedule is None:
        # 如果计划任务还没有启动,则启动计划任务
        if task_flag['run_flag'] == 'start_run':
            test_run_schedule = test_scheduler_obj().test_schedule
            test_run_schedule.add_job(
                task_run_test,      # 任务方法
                trigger='cron',
                second=cron_list[0],
                minute=cron_list[1],
                hour=cron_list[2],
                day=cron_list[3],
                week=cron_list[4],
                month=cron_list[5],
                id='schedule_test'
            )
            test_run_schedule.start()
    else:
        # 如果计划任务已经启动,有两个分支.
        # 1.修改当前任务的执行周期
        # 2.停止当前任务
        if task_flag['run_flag'] == 'start_run':
            test_run_schedule.resume()          # 计划任务恢复-对应任务暂停
            test_run_schedule.reschedule_job(
                job_id='schedule_test',
                trigger='cron',
                second=cron_list[0],
                minute=cron_list[1],
                hour=cron_list[2],
                day=cron_list[3],
                week=cron_list[4],
                month=cron_list[5]
            )
        elif task_flag['run_flag'] == 'stop_run':
            test_run_schedule.pause()           # 计划任务暂停

    return render(request, template_name='test_operate.html', context={})


def task_run_test():
    """
    调用测试方法
    :return:
    """
    print('定时操作_Task_Test ' + datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    # 运行测试
    VIKRunner.run_test()
    # 将测试报告的内容保存到DB
    handle_model.save_report_title()


def task_run_refresh_cookie():
    """
    调用更新Cookie方法
    :return:
    """
    print('定时操作_Task_Refresh_Cookie ' + datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    print(os.path.join(os.path.dirname(__file__), 'static', 'testcase'))
    GetUserCookie.search_cookie(os.path.join(os.path.dirname(__file__), 'static', 'testcase'))
