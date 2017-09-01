# -*- coding: utf-8 -*-
__author__ = 'Peng.Zhao'

from yattag import Doc


def create_mail_template(host_check_status_dict):
    b_status_list = host_check_status_dict['B_Client']
    c_status_list = host_check_status_dict['C_Client']
    h_status_list = host_check_status_dict['H_Client']
    j_status_list = host_check_status_dict['J_Client']
    w_status_list = host_check_status_dict['W_Client']
    m_status_list = host_check_status_dict['M_Client']

    doc, tag, text = Doc().tagtext()

    with tag('html'):
        with tag('head'):
            with tag('meta', ('http-equiv', 'Content-Type'), ('content', 'text/html; charset=UTF-8')):
                pass
        with tag('body'):
            with tag('table', ('width', '1640'), ('border', '0'), ('align', 'center'), ('cellpadding', '0'),
                     ('cellspacing', '0'), ('style', 'font-size:12px;font-family:SimSun;border:1px solid rgb(153,153,153);')):
                with tag('tr'):
                    with tag('td', ('colspan', '6'), ('style', 'height:60px;line-height:60px;font-size: 28px;padding-left: 20px;border-bottom:2px solid #000;')):
                        text('巡检结果')
                with tag('tr'):
                    with tag('td', ('colspan', '6'), ('style', 'height:40px;line-height:40px;font-size: 22px;padding-left: 20px;border-bottom:1px solid #d8d8d8;font-weight: bold;')):
                        text('C端')
                with tag('tr'):
                    for c_status in c_status_list:
                        with tag('td', ('style', 'padding-left: 20px;padding-top:20px;')):
                            with tag('table', ('cellpadding', '0'), ('cellspacing', '0'), ('style', 'border:1px solid #ccc;')):
                                with tag('tbody'):
                                    with tag('tr'):
                                        with tag('td', ('height', '30'), ('width', '80'), ('align', 'left'),
                                                 ('style', 'color:#646464;font-size:14px;border-top:1px solid #efeee7;border-bottom:1px solid #efeee7;font-weight:bold;padding-left: 10px;')):
                                            text('服务IP:')
                                        with tag('td', ('height', '30'), ('width', '120'), ('align', 'left'),
                                                 ('style', 'color:#ff6600;font-size:14px;border-top:1px solid #efeee7;border-bottom:1px solid #efeee7;font-weight:bold;')):
                                            with tag('a', ('href','http://monitor.highpin.cn/monitor/detail_report/?report_name={0}'.format(c_status['report_name']))):
                                                text(c_status['ip'])
                                    with tag('tr'):
                                        with tag('td', ('height', '30'), ('width', '80'), ('align', 'left'),
                                                 ('style', 'color:#646464;font-size:14px;border-top:1px solid #efeee7;border-bottom:1px solid #efeee7;font-weight:bold;padding-left: 10px;')):
                                            text('系统错误:')
                                        with tag('td', ('height', '30'), ('width', '120'), ('align', 'left'),
                                                 ('style', 'color:red;font-size:14px;border-top:1px solid #efeee7;border-bottom:1px solid #efeee7;font-weight:bold;')):
                                            text(c_status['status']['error'])
                                    with tag('tr'):
                                        with tag('td', ('height', '30'), ('width', '80'), ('align', 'left'),
                                                 ('style', 'color:#646464;font-size:14px;border-top:1px solid #efeee7;border-bottom:1px solid #efeee7;font-weight:bold;padding-left: 10px;')):
                                            text('验证失败:')
                                        with tag('td', ('height', '30'), ('width', '120'), ('align', 'left'),
                                                 ('style', 'color:#6d6d00;font-size:14px;border-top:1px solid #efeee7;border-bottom:1px solid #efeee7;font-weight:bold;')):
                                            text(c_status['status']['failure'])
                                    with tag('tr'):
                                        with tag('td', ('height', '30'), ('width', '80'), ('align', 'left'),
                                                 ('style', 'color:#646464;font-size:14px;border-top:1px solid #efeee7;border-bottom:1px solid #efeee7;font-weight:bold;padding-left: 10px;')):
                                            text('测试通过:')
                                        with tag('td', ('height', '30'), ('width', '120'), ('align', 'left'),
                                                 ('style', 'color:green;font-size:14px;border-top:1px solid #efeee7;border-bottom:1px solid #efeee7;font-weight:bold;')):
                                            text(c_status['status']['success'])
                with tag('tr'):
                    with tag('td', ('colspan', '6'), ('style', 'height:40px;line-height:40px;font-size: 22px;padding-left: 20px;border-bottom:1px solid #d8d8d8;font-weight: bold;')):
                        text('H端')
                    with tag('tr'):
                        for h_status in h_status_list:
                            with tag('td', ('style', 'padding-left: 20px;padding-top:20px;')):
                                with tag('table', ('cellpadding', '0'), ('cellspacing', '0'),
                                         ('style', 'border:1px solid #ccc;')):
                                    with tag('tbody'):
                                        with tag('tr'):
                                            with tag('td', ('height', '30'), ('width', '80'), ('align', 'left'),
                                                     ('style',
                                                      'color:#646464;font-size:14px;border-top:1px solid #efeee7;border-bottom:1px solid #efeee7;font-weight:bold;padding-left: 10px;')):
                                                text('服务IP:')
                                            with tag('td', ('height', '30'), ('width', '120'), ('align', 'left'),
                                                     ('style',
                                                      'color:#ff6600;font-size:14px;border-top:1px solid #efeee7;border-bottom:1px solid #efeee7;font-weight:bold;')):
                                                with tag('a', ('href', 'http://monitor.highpin.cn/monitor/detail_report/?report_name={0}'.format(h_status['report_name']))):
                                                    text(h_status['ip'])
                                        with tag('tr'):
                                            with tag('td', ('height', '30'), ('width', '80'), ('align', 'left'),
                                                     ('style',
                                                      'color:#646464;font-size:14px;border-top:1px solid #efeee7;border-bottom:1px solid #efeee7;font-weight:bold;padding-left: 10px;')):
                                                text('系统错误:')
                                            with tag('td', ('height', '30'), ('width', '120'), ('align', 'left'),
                                                     ('style',
                                                      'color:red;font-size:14px;border-top:1px solid #efeee7;border-bottom:1px solid #efeee7;font-weight:bold;')):
                                                text(h_status['status']['error'])
                                        with tag('tr'):
                                            with tag('td', ('height', '30'), ('width', '80'), ('align', 'left'),
                                                     ('style',
                                                      'color:#646464;font-size:14px;border-top:1px solid #efeee7;border-bottom:1px solid #efeee7;font-weight:bold;padding-left: 10px;')):
                                                text('验证失败:')
                                            with tag('td', ('height', '30'), ('width', '120'), ('align', 'left'),
                                                     ('style',
                                                      'color:#6d6d00;font-size:14px;border-top:1px solid #efeee7;border-bottom:1px solid #efeee7;font-weight:bold;')):
                                                text(h_status['status']['failure'])
                                        with tag('tr'):
                                            with tag('td', ('height', '30'), ('width', '80'), ('align', 'left'),
                                                     ('style',
                                                      'color:#646464;font-size:14px;border-top:1px solid #efeee7;border-bottom:1px solid #efeee7;font-weight:bold;padding-left: 10px;')):
                                                text('测试通过:')
                                            with tag('td', ('height', '30'), ('width', '120'), ('align', 'left'),
                                                     ('style',
                                                      'color:green;font-size:14px;border-top:1px solid #efeee7;border-bottom:1px solid #efeee7;font-weight:bold;')):
                                                text(h_status['status']['success'])
                with tag('tr'):
                    with tag('td', ('colspan', '6'), ('style', 'height:40px;line-height:40px;font-size: 22px;padding-left: 20px;border-bottom:1px solid #d8d8d8;font-weight: bold;')):
                        text('J端')
                    with tag('tr'):
                        for j_status in j_status_list:
                            with tag('td', ('style', 'padding-left: 20px;padding-top:20px;')):
                                with tag('table', ('cellpadding', '0'), ('cellspacing', '0'),
                                         ('style', 'border:1px solid #ccc;')):
                                    with tag('tbody'):
                                        with tag('tr'):
                                            with tag('td', ('height', '30'), ('width', '80'), ('align', 'left'),
                                                     ('style',
                                                      'color:#646464;font-size:14px;border-top:1px solid #efeee7;border-bottom:1px solid #efeee7;font-weight:bold;padding-left: 10px;')):
                                                text('服务IP:')
                                            with tag('td', ('height', '30'), ('width', '120'), ('align', 'left'),
                                                     ('style',
                                                      'color:#ff6600;font-size:14px;border-top:1px solid #efeee7;border-bottom:1px solid #efeee7;font-weight:bold;')):
                                                with tag('a', ('href','http://monitor.highpin.cn/monitor/detail_report/?report_name={0}'.format(j_status['report_name']))):
                                                    text(j_status['ip'])
                                        with tag('tr'):
                                            with tag('td', ('height', '30'), ('width', '80'), ('align', 'left'),
                                                     ('style',
                                                      'color:#646464;font-size:14px;border-top:1px solid #efeee7;border-bottom:1px solid #efeee7;font-weight:bold;padding-left: 10px;')):
                                                text('系统错误:')
                                            with tag('td', ('height', '30'), ('width', '120'), ('align', 'left'),
                                                     ('style',
                                                      'color:red;font-size:14px;border-top:1px solid #efeee7;border-bottom:1px solid #efeee7;font-weight:bold;')):
                                                text(j_status['status']['error'])
                                        with tag('tr'):
                                            with tag('td', ('height', '30'), ('width', '80'), ('align', 'left'),
                                                     ('style',
                                                      'color:#646464;font-size:14px;border-top:1px solid #efeee7;border-bottom:1px solid #efeee7;font-weight:bold;padding-left: 10px;')):
                                                text('验证失败:')
                                            with tag('td', ('height', '30'), ('width', '120'), ('align', 'left'),
                                                     ('style',
                                                      'color:#6d6d00;font-size:14px;border-top:1px solid #efeee7;border-bottom:1px solid #efeee7;font-weight:bold;')):
                                                text(j_status['status']['failure'])
                                        with tag('tr'):
                                            with tag('td', ('height', '30'), ('width', '80'), ('align', 'left'),
                                                     ('style',
                                                      'color:#646464;font-size:14px;border-top:1px solid #efeee7;border-bottom:1px solid #efeee7;font-weight:bold;padding-left: 10px;')):
                                                text('测试通过:')
                                            with tag('td', ('height', '30'), ('width', '120'), ('align', 'left'),
                                                     ('style',
                                                      'color:green;font-size:14px;border-top:1px solid #efeee7;border-bottom:1px solid #efeee7;font-weight:bold;')):
                                                text(j_status['status']['success'])
                with tag('tr'):
                    with tag('td', ('colspan', '6'), ('style', 'height:40px;line-height:40px;font-size: 22px;padding-left: 20px;border-bottom:1px solid #d8d8d8;font-weight: bold;')):
                        text('W端')
                    with tag('tr'):
                        for w_status in w_status_list:
                            with tag('td', ('style', 'padding-left: 20px;padding-top:20px;')):
                                with tag('table', ('cellpadding', '0'), ('cellspacing', '0'),
                                         ('style', 'border:1px solid #ccc;')):
                                    with tag('tbody'):
                                        with tag('tr'):
                                            with tag('td', ('height', '30'), ('width', '80'), ('align', 'left'),
                                                     ('style',
                                                      'color:#646464;font-size:14px;border-top:1px solid #efeee7;border-bottom:1px solid #efeee7;font-weight:bold;padding-left: 10px;')):
                                                text('服务IP:')
                                            with tag('td', ('height', '30'), ('width', '120'), ('align', 'left'),
                                                     ('style',
                                                      'color:#ff6600;font-size:14px;border-top:1px solid #efeee7;border-bottom:1px solid #efeee7;font-weight:bold;')):
                                                with tag('a', ('href', 'http://monitor.highpin.cn/monitor/detail_report/?report_name={0}'.format(w_status['report_name']))):
                                                    text(w_status['ip'])
                                        with tag('tr'):
                                            with tag('td', ('height', '30'), ('width', '80'), ('align', 'left'),
                                                     ('style',
                                                      'color:#646464;font-size:14px;border-top:1px solid #efeee7;border-bottom:1px solid #efeee7;font-weight:bold;padding-left: 10px;')):
                                                text('系统错误:')
                                            with tag('td', ('height', '30'), ('width', '120'), ('align', 'left'),
                                                     ('style',
                                                      'color:red;font-size:14px;border-top:1px solid #efeee7;border-bottom:1px solid #efeee7;font-weight:bold;')):
                                                text(w_status['status']['error'])
                                        with tag('tr'):
                                            with tag('td', ('height', '30'), ('width', '80'), ('align', 'left'),
                                                     ('style',
                                                      'color:#646464;font-size:14px;border-top:1px solid #efeee7;border-bottom:1px solid #efeee7;font-weight:bold;padding-left: 10px;')):
                                                text('验证失败:')
                                            with tag('td', ('height', '30'), ('width', '120'), ('align', 'left'),
                                                     ('style',
                                                      'color:#6d6d00;font-size:14px;border-top:1px solid #efeee7;border-bottom:1px solid #efeee7;font-weight:bold;')):
                                                text(w_status['status']['failure'])
                                        with tag('tr'):
                                            with tag('td', ('height', '30'), ('width', '80'), ('align', 'left'),
                                                     ('style',
                                                      'color:#646464;font-size:14px;border-top:1px solid #efeee7;border-bottom:1px solid #efeee7;font-weight:bold;padding-left: 10px;')):
                                                text('测试通过:')
                                            with tag('td', ('height', '30'), ('width', '120'), ('align', 'left'),
                                                     ('style',
                                                      'color:green;font-size:14px;border-top:1px solid #efeee7;border-bottom:1px solid #efeee7;font-weight:bold;')):
                                                text(w_status['status']['success'])
                with tag('tr'):
                    with tag('td', ('colspan', '6'), ('style', 'height:40px;line-height:40px;font-size: 22px;padding-left: 20px;border-bottom:1px solid #d8d8d8;font-weight: bold;')):
                        text('B端')
                    with tag('tr'):
                        for b_status in b_status_list:
                            with tag('td', ('style', 'padding-left: 20px;padding-top:20px;')):
                                with tag('table', ('cellpadding', '0'), ('cellspacing', '0'),
                                         ('style', 'border:1px solid #ccc;')):
                                    with tag('tbody'):
                                        with tag('tr'):
                                            with tag('td', ('height', '30'), ('width', '80'), ('align', 'left'),
                                                     ('style',
                                                      'color:#646464;font-size:14px;border-top:1px solid #efeee7;border-bottom:1px solid #efeee7;font-weight:bold;padding-left: 10px;')):
                                                text('服务IP:')
                                            with tag('td', ('height', '30'), ('width', '120'), ('align', 'left'),
                                                     ('style',
                                                      'color:#ff6600;font-size:14px;border-top:1px solid #efeee7;border-bottom:1px solid #efeee7;font-weight:bold;')):
                                                with tag('a', ('href', 'http://monitor.highpin.cn/monitor/detail_report/?report_name={0}'.format(b_status['report_name']))):
                                                    text(b_status['ip'])
                                        with tag('tr'):
                                            with tag('td', ('height', '30'), ('width', '80'), ('align', 'left'),
                                                     ('style',
                                                      'color:#646464;font-size:14px;border-top:1px solid #efeee7;border-bottom:1px solid #efeee7;font-weight:bold;padding-left: 10px;')):
                                                text('系统错误:')
                                            with tag('td', ('height', '30'), ('width', '120'), ('align', 'left'),
                                                     ('style', 'color:red;font-size:14px;border-top:1px solid #efeee7;border-bottom:1px solid #efeee7;font-weight:bold;')):
                                                text(b_status['status']['error'])
                                        with tag('tr'):
                                            with tag('td', ('height', '30'), ('width', '80'), ('align', 'left'),
                                                     ('style',
                                                      'color:#646464;font-size:14px;border-top:1px solid #efeee7;border-bottom:1px solid #efeee7;font-weight:bold;padding-left: 10px;')):
                                                text('验证失败:')
                                            with tag('td', ('height', '30'), ('width', '120'), ('align', 'left'),
                                                     ('style',
                                                      'color:#6d6d00;font-size:14px;border-top:1px solid #efeee7;border-bottom:1px solid #efeee7;font-weight:bold;')):
                                                text(b_status['status']['failure'])
                                        with tag('tr'):
                                            with tag('td', ('height', '30'), ('width', '80'), ('align', 'left'),
                                                     ('style',
                                                      'color:#646464;font-size:14px;border-top:1px solid #efeee7;border-bottom:1px solid #efeee7;font-weight:bold;padding-left: 10px;')):
                                                text('测试通过:')
                                            with tag('td', ('height', '30'), ('width', '120'), ('align', 'left'),
                                                     ('style',
                                                      'color:green;font-size:14px;border-top:1px solid #efeee7;border-bottom:1px solid #efeee7;font-weight:bold;')):
                                                text(b_status['status']['success'])
                    with tag('tr'):
                        with tag('td', ('colspan', '6'), ('style', 'height:40px;line-height:40px;font-size: 22px;padding-left: 20px;border-bottom:1px solid #d8d8d8;font-weight: bold;')):
                            text('M端')
                        with tag('tr'):
                            for m_status in m_status_list:
                                with tag('td',
                                         ('style', 'padding-left: 20px;padding-top:20px;')):
                                    with tag('table', ('cellpadding', '0'),
                                             ('cellspacing', '0'),
                                             ('style', 'border:1px solid #ccc;')):
                                        with tag('tbody'):
                                            with tag('tr'):
                                                with tag('td', ('height', '30'),
                                                         ('width', '80'), ('align', 'left'),
                                                         ('style',
                                                          'color:#646464;font-size:14px;border-top:1px solid #efeee7;border-bottom:1px solid #efeee7;font-weight:bold;padding-left: 10px;')):
                                                    text('服务IP:')
                                                with tag('td', ('height', '30'),
                                                         ('width', '120'), ('align', 'left'),
                                                         ('style',
                                                          'color:#ff6600;font-size:14px;border-top:1px solid #efeee7;border-bottom:1px solid #efeee7;font-weight:bold;')):
                                                    with tag('a', ('href', 'http://monitor.highpin.cn/monitor/detail_report/?report_name={0}'.format(m_status['report_name']))):
                                                        text(m_status['ip'])
                                            with tag('tr'):
                                                with tag('td', ('height', '30'),
                                                         ('width', '80'), ('align', 'left'),
                                                         ('style',
                                                          'color:#646464;font-size:14px;border-top:1px solid #efeee7;border-bottom:1px solid #efeee7;font-weight:bold;padding-left: 10px;')):
                                                    text('系统错误:')
                                                with tag('td', ('height', '30'),
                                                         ('width', '120'), ('align', 'left'),
                                                         ('style',
                                                          'color:red;font-size:14px;border-top:1px solid #efeee7;border-bottom:1px solid #efeee7;font-weight:bold;')):
                                                    text(m_status['status']['error'])
                                            with tag('tr'):
                                                with tag('td', ('height', '30'),
                                                         ('width', '80'), ('align', 'left'),
                                                         ('style',
                                                          'color:#646464;font-size:14px;border-top:1px solid #efeee7;border-bottom:1px solid #efeee7;font-weight:bold;padding-left: 10px;')):
                                                    text('验证失败:')
                                                with tag('td', ('height', '30'),
                                                         ('width', '120'), ('align', 'left'),
                                                         ('style',
                                                          'color:#6d6d00;font-size:14px;border-top:1px solid #efeee7;border-bottom:1px solid #efeee7;font-weight:bold;')):
                                                    text(m_status['status']['failure'])
                                            with tag('tr'):
                                                with tag('td', ('height', '30'),
                                                         ('width', '80'), ('align', 'left'),
                                                         ('style',
                                                          'color:#646464;font-size:14px;border-top:1px solid #efeee7;border-bottom:1px solid #efeee7;font-weight:bold;padding-left: 10px;')):
                                                    text('测试通过:')
                                                with tag('td', ('height', '30'),
                                                         ('width', '120'), ('align', 'left'),
                                                         ('style',
                                                          'color:green;font-size:14px;border-top:1px solid #efeee7;border-bottom:1px solid #efeee7;font-weight:bold;')):
                                                    text(m_status['status']['success'])
                with tag('tr'):     #空出一行
                    with tag('td', ('colspan', '6'), ('style', 'height:40px;line-height:40px;font-size: 22px;padding-left: 20px;border-bottom:1px solid #d8d8d8;font-weight: bold;')):
                        pass
    return doc

if __name__ == '__main__':
    doc = create_mail_template()
    print(doc.getvalue())