# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-10 06:18
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20170310_0604'),
    ]

    operations = [
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer_content', models.TextField()),
                ('is_correct', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question_content', models.TextField()),
            ],
        ),
        migrations.RenameModel(
            old_name='Levels',
            new_name='Level',
        ),
        migrations.DeleteModel(
            name='Answers',
        ),
        migrations.DeleteModel(
            name='Questions',
        ),
        migrations.AddField(
            model_name='question',
            name='level_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.Level'),
        ),
        migrations.AddField(
            model_name='answer',
            name='question_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.Question'),
        ),
    ]