# -*- coding: utf-8 -*-
# Generated by Django 1.11.25 on 2019-11-03 14:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('canchas', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='cancha',
            name='desde_martes',
            field=models.TimeField(blank=True, null=True),
        ),
    ]
