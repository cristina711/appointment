# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-10-29 01:27
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('appointmentapp', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='birthday',
        ),
    ]
