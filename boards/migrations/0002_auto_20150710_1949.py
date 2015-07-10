# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('boards', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='list',
            old_name='boards',
            new_name='board',
        ),
        migrations.AddField(
            model_name='board',
            name='is_public',
            field=models.BooleanField(default=False),
        ),
    ]
