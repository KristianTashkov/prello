from django.db import models
from django.contrib import auth


def get_boards(self):
    return self.boards.all()


def get_created_boards(self):
    return self.created_boards.all()


def get_other_boards(self):
    return [board for board in self.get_boards()
            if board not in self.get_created_boards()]


def is_admin(self, board):
    return self in board.admins.all()

auth.models.User.add_to_class('get_boards', get_boards)
auth.models.User.add_to_class('get_created_boards', get_created_boards)
auth.models.User.add_to_class('get_other_boards', get_other_boards)
auth.models.User.add_to_class('is_admin', is_admin)
