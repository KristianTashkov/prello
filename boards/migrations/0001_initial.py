# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Board',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('is_public', models.BooleanField(default=False)),
                ('admins', models.ManyToManyField(related_name='administrator_of', to=settings.AUTH_USER_MODEL)),
                ('creator', models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='created_boards')),
                ('members', models.ManyToManyField(related_name='boards', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('timestamp', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='List',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('board', models.ForeignKey(to='boards.Board', related_name='lists')),
            ],
        ),
        migrations.CreateModel(
            name='ListEntry',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('description', models.TextField()),
                ('due_date', models.DateField(blank=True, null=True)),
                ('members', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
                ('parent_list', models.ForeignKey(to='boards.List', related_name='entries')),
            ],
        ),
        migrations.AddField(
            model_name='comment',
            name='list_entry',
            field=models.ForeignKey(to='boards.ListEntry', related_name='comments'),
        ),
        migrations.AddField(
            model_name='comment',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='comments'),
        ),
    ]
