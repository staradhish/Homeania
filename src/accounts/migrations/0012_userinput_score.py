# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-20 14:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0011_auto_20170320_1344'),
    ]

    operations = [
        migrations.AddField(
            model_name='userinput',
            name='score',
            field=models.IntegerField(default=0),
        ),
    ]