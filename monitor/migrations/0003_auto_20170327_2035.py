# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-27 12:35
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('monitor', '0002_auto_20170327_2034'),
    ]

    operations = [
        migrations.RenameField(
            model_name='item',
            old_name='is_error',
            new_name='error_flag',
        ),
    ]