# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-06-26 20:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myadmin', '0004_auto_20180626_2036'),
    ]

    operations = [
        migrations.AddField(
            model_name='goods',
            name='store',
            field=models.IntegerField(default=0),
        ),
    ]
