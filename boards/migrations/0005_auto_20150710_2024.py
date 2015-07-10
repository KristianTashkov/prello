# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('boards', '0004_auto_20150710_2021'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listentry',
            name='due_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
