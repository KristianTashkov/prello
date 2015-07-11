from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

from boards.models import *


class TestCalls(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create(username="admin")
        self.user.set_password("123")
        self.user.save()

        self.assertTrue(self.client.login(username="admin", password="123"))

    def test_empty_boards_request(self):
        response = self.client.get(reverse('boards'))
        self.assertEqual(response.status_code, 200)

        self.assertTrue("boards/boards.html" in
                        [template.name for template in response.templates])

        self.assertEquals(len(response.context["created_boards"]), 0)
        self.assertEquals(len(response.context["other_boards"]), 0)

    def test_single_board_boards_request(self):
        b = Board.objects.create(title="asd", creator=self.user)
        b.members.add(self.user)

        response = self.client.get(reverse('boards'))

        self.assertEquals(len(response.context["created_boards"]), 1)
        self.assertEquals(len(response.context["other_boards"]), 0)

    def test_single_board_boards_request(self):
        other_user = User.objects.create(username="username")

        b = Board.objects.create(title="asd", creator=other_user)
        b.members.add(self.user)

        response = self.client.get(reverse('boards'))

        self.assertEquals(len(response.context["created_boards"]), 0)
        self.assertEquals(len(response.context["other_boards"]), 1)

    def test_board_request(self):
        b = Board.objects.create(title="asd", creator=self.user)
        b.members.add(self.user)

        response = self.client.get(reverse('board', args=[1]))
        self.assertEqual(response.status_code, 200)

        self.assertTrue("boards/board.html" in
                        [template.name for template in response.templates])

        self.assertEquals(response.context["board"].id, 1)
        self.assertEquals(response.context["is_admin"], False)

    def test_board_unauthorized_request(self):
        other_user = User.objects.create(username="username")

        b = Board.objects.create(title="asd", creator=other_user)

        response = self.client.get(reverse('board', args=[1]))
        self.assertFalse("boards/board.html" in
                         [template.name for template in response.templates])

    def test_new_board_request(self):
        response = self.client.post(reverse('new_board'),
                                    data={'board_title': 'title'})

        self.assertEquals(len(self.user.boards.all()), 1)

    def test_delete_board_request(self):
        b = Board.new(self.user, "title")

        self.assertEquals(len(self.user.boards.all()), 1)

        response = self.client.post(reverse('delete_board'),
                                    {'board_id': b.id})

        self.assertEquals(len(self.user.boards.all()), 0)

    def test_unauthorized_delete_board_request(self):
        other_user = User.objects.create(username="username")
        b = Board.new(other_user, "title")

        response = self.client.post(reverse('delete_board'),
                                    {'board_id': b.id})

        self.assertEquals(response.status_code, 404)

    def test_new_list_request(self):
        b = Board.new(self.user, "title")
        response = self.client.post(reverse('new_list'),
                                    data={'list_title': 'title',
                                          'board_id': b.id})

        self.assertEquals(len(b.lists.all()), 1)

    def test_list_board_request(self):
        b = Board.new(self.user, "title")
        l = List.objects.create(title="title", board=b)

        self.assertEquals(len(b.lists.all()), 1)

        response = self.client.post(reverse('delete_list'),
                                    {'list_id': l.id})

        self.assertEquals(len(b.lists.all()), 0)

    def test_unauthorized_delete_list_request(self):
        other_user = User.objects.create(username="username")
        b = Board.new(other_user, "title")
        l = List.objects.create(title="title", board=b)

        response = self.client.post(reverse('delete_list'),
                                    {'list_id': l.id})

        self.assertEquals(response.status_code, 404)

    def test_new_list_entry_request(self):
        b = Board.new(self.user, "title")
        l = List.objects.create(title="title", board=b)

        self.assertEquals(len(l.entries.all()), 0)

        response = self.client.post(reverse('new_list_item'),
                                    data={'list_item_title': 'title',
                                          'list_item_description': 'desc',
                                          'list_id': l.id})

        self.assertEquals(len(l.entries.all()), 1)

    def test_list_entry_board_request(self):
        b = Board.new(self.user, "title")
        l = List.objects.create(title="title", board=b)
        le = ListEntry.objects.create(title="title",
                                      description="",
                                      parent_list=l)

        self.assertEquals(len(l.entries.all()), 1)

        response = self.client.post(reverse('delete_list_item'),
                                    {'list_entry_id': le.id})

        self.assertEquals(len(l.entries.all()), 0)

    def test_unauthorized_delete_list_entry_request(self):
        other_user = User.objects.create(username="username")
        b = Board.new(other_user, "title")
        l = List.objects.create(title="title", board=b)
        le = ListEntry.objects.create(title="title",
                                      description="",
                                      parent_list=l)

        response = self.client.post(reverse('delete_list_item'),
                                    {'list_entry_id': le.id})

        self.assertEquals(response.status_code, 404)

    def test_change_list_item_request(self):
        b = Board.new(self.user, "title")
        l = List.objects.create(title="title", board=b)
        le = ListEntry.objects.create(title="title",
                                      description="",
                                      parent_list=l)

        response = self.client.post(reverse('change_entry'),
                                    {'list_entry_title': 'new_title',
                                     'list_entry_description': 'new_desc',
                                     'list_entry_id': le.id})

        le = ListEntry.objects.get(id=le.id)
        self.assertEquals(le.title, "new_title")
        self.assertEquals(le.description, "new_desc")

    def test_new_comment_request(self):
        b = Board.new(self.user, "title")
        l = List.objects.create(title="title", board=b)
        le = ListEntry.objects.create(title="title",
                                      description="",
                                      parent_list=l)

        response = self.client.post(reverse('post_comment'),
                                    {'comment': 'comment',
                                     'list_entry_id': le.id})

        self.assertEquals(le.comments.first().text, 'comment')

    def test_new_member_request(self):
        b = Board.new(self.user, "title")
        other_user = User.objects.create(username="username")

        self.assertEquals(len(other_user.boards.all()), 0)

        response = self.client.post(reverse('add_member'),
                                    {'member_username': 'username',
                                     'board_id': b.id})

        self.assertEquals(len(other_user.boards.all()), 1)

    def test_new_admin_request(self):
        b = Board.new(self.user, "title")
        other_user = User.objects.create(username="username")

        self.assertFalse(other_user.is_admin(b))
        self.assertEquals(len(other_user.boards.all()), 0)

        response = self.client.post(reverse('add_admin'),
                                    {'member_username': 'username',
                                     'board_id': b.id})

        self.assertEquals(len(other_user.boards.all()), 1)
        self.assertTrue(other_user.is_admin(b))

    def test_remove_member_request(self):
        b = Board.new(self.user, "title")
        other_user = User.objects.create(username="username")
        b.members.add(other_user)

        self.assertEquals(len(b.members.all()), 2)

        response = self.client.post(reverse('remove_member'),
                                    {'user_id': other_user.id,
                                     'board_id': b.id})

        self.assertEquals(len(b.members.all()), 1)

    def test_remove_admin_request(self):
        b = Board.new(self.user, "title")
        other_user = User.objects.create(username="username")
        b.members.add(other_user)
        b.admins.add(other_user)

        self.assertEquals(len(b.members.all()), 2)
        self.assertTrue(other_user.is_admin(b))

        response = self.client.post(reverse('remove_admin'),
                                    {'user_id': other_user.id,
                                     'board_id': b.id})

        self.assertEquals(len(b.members.all()), 2)
        self.assertFalse(other_user.is_admin(b))
