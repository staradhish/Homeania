# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-10 07:18
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_auto_20170310_0629'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myuser',
            name='level_id',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='accounts.Level'),
        ),
    ]
