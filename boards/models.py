from django.db import models
from django.conf import settings


class Board(models.Model):
    title = models.CharField(max_length=50)
    admins = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                    related_name='administrator_of')
    members = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                     related_name='boards')
    is_public = models.BooleanField(default=False)


class List(models.Model):
    title = models.CharField(max_length=50)
    board = models.ForeignKey(Board, related_name="lists")


class ListEntry(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField()
    parent_list = models.ForeignKey(List, related_name="entries")
    members = models.ManyToManyField(settings.AUTH_USER_MODEL)
    due_date = models.DateField(blank=True, null=True)


class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="comments")
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now=True)
