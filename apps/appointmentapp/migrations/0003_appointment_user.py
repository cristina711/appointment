# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-10-29 01:58
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('appointmentapp', '0002_remove_user_birthday'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointment',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='appointments', to='appointmentapp.User'),
            preserve_default=False,
        ),
    ]