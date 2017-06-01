# -*- coding: utf-8 -*-

__author__ = 'Peng.Zhao'

import os
import smtplib
import configparser
from email.header import Header
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from monitor.HighPin_VIK.ReportHandler.ReportHandler import report_compress, report_filter


def read_config(conf_path):
    """
    :description: 读取配置文件,并返回配置文件解析
    :param conf_path: 
    :return: 
    """
    file_path_name = conf_path
    parse = configparser.ConfigParser()
    parse.read(file_path_name, encoding='UTF-8')
    return parse


def send_email_html_content(parse_info, flag):
    """
    :description: 编辑邮件正文,并且发送邮件
    :param parse_info: 邮箱配置信息
    :return:
    """
    # 确定报告存放路径
    # report_folder_path = os.path.abspath('monitor/static/report')
    report_folder_path = os.path.join(os.path.abspath('.'), 'monitor', 'static', 'report')

    host = parse_info.get('smtp_host_info', 'host')
    port = parse_info.getint('smtp_host_info', 'port')

    username = parse_info.get('sender_info', 'username')
    password = parse_info.get('sender_info', 'password')

    sender = parse_info.get('email_info', 'sender')
    receiver = parse_info.get('email_info', 'receiver')
    subject = parse_info.get('email_info', 'subject')

    # 定义邮件框架
    msg = MIMEMultipart()

    # 添加邮件附件
    report_attach_name = select_report(report_folder_path)
    # 获取报告的绝对路径
    report_full_path = report_folder_path + os.sep + report_attach_name
    # 对文件进行压缩
    zip_report_full_path = report_compress(report_full_path)

    report_attach = open(zip_report_full_path, 'rb')
    mst_attach = MIMEText(report_attach.read(), 'base64', _charset='UTF-8')
    mst_attach['Content-Type'] = 'application/octet-stream'
    mst_attach['Content-Disposition'] = 'attachment; filename=' + zip_report_full_path.split(os.sep)[-1]
    msg.attach(mst_attach)

    # 使用内嵌HTML的格式
    # 对HTML报告进行过滤
    lite_report_path = report_filter(report_full_path)
    lite_report_handler = open(lite_report_path, mode='r', encoding='UTF-8')
    lite_report_html_content = lite_report_handler.read()
    # 修改邮件正文的字体大小
    lite_report_html_content = lite_report_html_content.replace('font-size: 80%', 'font-size: 100%')

    # 添加邮件正文(HTML)
    mst_text = MIMEText(lite_report_html_content, _subtype='html', _charset='UTF-8')
    msg.attach(mst_text)

    # 添加邮件标题
    if flag:
        msg['Subject'] = Header(subject, 'UTF-8')
    else:
        msg['Subject'] = Header('Error!!!-' + subject, 'UTF-8')
    msg['from'] = sender
    msg['to'] = receiver
    # 给多个人发送需要使用列表
    receiver_list = receiver.split(',')

    # 发送邮件(SSL)
    smtp = smtplib.SMTP_SSL(host=host, port=port)
    # smtp = smtplib.SMTP(host=host, port=port)
    smtp.login(username, password)
    smtp.sendmail(sender, receiver_list, msg.as_string())
    smtp.quit()


def select_report(file_path):
    # 选择文件夹中最新的一份儿文件
    report_list = os.listdir(file_path)
    report_list = sorted(report_list)
    return report_list[-1]


def send_report(configure_path, error_count, failure_count):
    p_info = read_config(configure_path)
    # send_email(p_info)
    # 如果报告中没有出现错误,则flag置为True.
    if error_count == 0 and failure_count == 0:
        send_email_html_content(p_info, True)
    else:
        send_email_html_content(p_info, False)

if __name__ == '__main__':
    print(os.path.abspath('../../static/report'))
    pass

