# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-24 03:32
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('model_name', models.CharField(max_length=300, verbose_name='模块名称')),
                ('record_time', models.DateField(verbose_name='记录日期')),
                ('is_error', models.BooleanField(default=False, verbose_name='是否有错')),
            ],
        ),
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('report_name', models.CharField(max_length=200, verbose_name='报告名称')),
                ('create_date', models.DateField(verbose_name='生成日期')),
                ('create_time', models.TimeField(verbose_name='生成时间')),
                ('is_error', models.BooleanField(default=False, verbose_name='是否有错')),
            ],
            options={
                'ordering': ['-create_date'],
            },
        ),
        migrations.AddField(
            model_name='item',
            name='report',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='monitor.Report'),
        ),
    ]