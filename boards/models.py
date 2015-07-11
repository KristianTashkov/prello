from django.db import models
from django.conf import settings


class Board(models.Model):
    title = models.CharField(max_length=50)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL,
                                related_name="created_boards")
    admins = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                    related_name='administrator_of')
    members = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                     related_name='boards')
    is_public = models.BooleanField(default=False)

    def new(user, title):
        board = Board(title=title, creator=user)
        board.save()

        board.admins.add(user)
        board.members.add(user)
        return board

    def get_for_rendering(self):
        self.board_members = self.members.all()
        self.board_admins = self.admins.all()
        self.board_lists = [board_list.get_for_rendering()
                            for board_list in self.lists.all()]
        return self


class List(models.Model):
    title = models.CharField(max_length=50)
    board = models.ForeignKey(Board, related_name="lists")

    def get_for_rendering(self):
        self.list_entries = [entry.get_for_rendering() for entry in
                             self.entries.all()]
        return self


class ListEntry(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField()
    parent_list = models.ForeignKey(List, related_name="entries")
    members = models.ManyToManyField(settings.AUTH_USER_MODEL)
    due_date = models.DateField(blank=True, null=True)

    def get_for_rendering(self):
        self.members = self.members.all()
        self.user_comments = self.comments.all()
        return self


class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="comments")
    list_entry = models.ForeignKey(ListEntry, related_name="comments")
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now=True)
