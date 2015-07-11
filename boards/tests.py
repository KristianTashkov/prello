from django.test import TestCase, Client
from django.contrib.auth.models import User

from boards.models import *


class TestCalls(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create(username="admin")
        self.user.set_password("123")
        self.user.save()

        self.assertTrue(self.client.login(username="admin", password="123"))

    def test_empty_boards_request(self):
        response = self.client.get('/boards', follow=True)
        self.assertEqual(response.status_code, 200)

        self.assertTrue("boards/boards.html" in
                        [template.name for template in response.templates])

        self.assertEquals(len(response.context["created_boards"]), 0)
        self.assertEquals(len(response.context["other_boards"]), 0)

    def test_single_board_boards_request(self):
        b = Board.objects.create(title="asd", creator=self.user)
        b.members.add(self.user)

        response = self.client.get('/boards', follow=True)

        self.assertEquals(len(response.context["created_boards"]), 1)
        self.assertEquals(len(response.context["other_boards"]), 0)

    def test_single_board_boards_request(self):
        other_user = User.objects.create(username="username")

        b = Board.objects.create(title="asd", creator=other_user)
        b.members.add(self.user)

        response = self.client.get('/boards', follow=True)

        self.assertEquals(len(response.context["created_boards"]), 0)
        self.assertEquals(len(response.context["other_boards"]), 1)

    def test_board_request(self):
        b = Board.objects.create(title="asd", creator=self.user)
        b.members.add(self.user)

        response = self.client.get('/boards/1', follow=True)
        self.assertEqual(response.status_code, 200)

        self.assertTrue("boards/board.html" in
                        [template.name for template in response.templates])

        self.assertEquals(response.context["board"].id, 1)
        self.assertEquals(response.context["is_admin"], False)

    def test_board_unauthorized_request(self):
        other_user = User.objects.create(username="username")

        b = Board.objects.create(title="asd", creator=other_user)

        response = self.client.get('/boards/1', follow=True)
        self.assertFalse("boards/board.html" in
                         [template.name for template in response.templates])

    def test_new_board_request(self):
        response = self.client.post('/boards/new',
                                    data={'board_title': 'title'},
                                    follow=True)
        print(response.redirect_chain)

        self.assertEquals(len(self.user.boards.all()), 1)
