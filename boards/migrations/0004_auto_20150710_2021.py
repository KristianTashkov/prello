# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('boards', '0003_comment_listentry'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listentry',
            name='parent_list',
            field=models.ForeignKey(related_name='entries', to='boards.List'),
        ),
    ]
