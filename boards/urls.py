from django.conf.urls import include, url
from django.contrib import admin
from . import views

urlpatterns = [
    url(r'(?P<board_id>[0-9]+)/$', views.board, name="board"),
    url(r'^new/$', views.new_board, name="new_board"),
    url(r'^delete/$', views.delete_board, name="delete_board"),
    url(r'^list/new/$', views.new_list, name="new_list"),
    url(r'^list/delete/$', views.delete_list, name="delete_list"),
    url(r'^list/move/$', views.move_list, name="move_list"),
    url(r'^list_item/new/$', views.new_list_item, name="new_list_item"),
    url(r'^list_item/move/$', views.move_list_item, name="move_list_item"),
    url(r'^list_item/delete/$', views.delete_list_item,
        name="delete_list_item"),
    url(r'^list_item/change/$', views.change_list_item, name="change_entry"),
    url(r'^list_item/post_comment/$', views.post_comment,
        name="post_comment"),
    url(r'^member/new/$', views.new_member, name="add_member"),
    url(r'^member/admin/new/$', views.new_admin, name="add_admin"),
    url(r'^member/remove/$', views.remove_member, name="remove_member"),
    url(r'^member/admin/remove/$', views.remove_admin, name="remove_admin"),
    url(r'^$', views.boards, name="boards"),
]
