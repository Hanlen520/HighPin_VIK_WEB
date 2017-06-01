from django.db import models

# Create your models here.


class Report(models.Model):
    report_name = models.CharField('报告名称', max_length=200)
    create_date = models.DateField('生成日期')
    create_time = models.TimeField('生成时间')
    is_error = models.BooleanField('是否有错', default=False)

    def __str__(self):
        return self.report_name

    class Meta:
        # 表示按照时间逆序倒排
        ordering = ['-create_date', '-create_time']


class Item(models.Model):
    report = models.ForeignKey(Report, on_delete=models.CASCADE)
    model_name = models.CharField('模块名称', max_length=300)
    record_date = models.DateField('记录日期')
    error_flag = models.IntegerField('服务错误标志位')

    def __str__(self):
        return self.model_name

    class Meta:
        ordering = ['-report']  # 按照外键倒排


class Item_Error(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    model_name = models.CharField('模块名称', max_length=300)
    item_name = models.CharField('条目名称', max_length=300)
    error_type_flag = models.IntegerField('错误类型')
    record_date = models.DateField('记录时间')

    def __str__(self):
        return self.item_name

    class Meta:
        ordering = ['-item']    # 按照外键倒排


class Case(models.Model):
    case_name = models.CharField('用例名称', max_length=300)
    case_time = models.DateTimeField('上传时间')

    def __str__(self):
        return self.case_name

    class Meta:
        ordering = ['-case_name']   # 按照用例名称排序
