from django.conf.urls import url
from monitor import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^reports_list/', views.reports_list, name='reports_list'),
    url(r'^items_list/', views.get_new_report_items, name='items_list'),
    url(r'^display_chart/', views.display_chart, name='display_chart'),
    url(r'^cases_list/', views.cases_list, name='cases_list'),
    url(r'^upload_case/', views.upload_case, name='upload_case'),
    url(r'^delete_case/', views.delete_case, name='delete_case'),
    url(r'^test_operate/', views.test_operate, name='test_operate'),
    url(r'^run_test/', views.run_test, name='run_test'),
    url(r'^refresh_cookie/', views.refresh_cookie, name='refresh_cookie'),
    url(r'^timing_task/', views.timing_task, name='timing_task'),
]

