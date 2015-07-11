from django.conf.urls import include, url
from django.contrib import admin
from . import views

urlpatterns = [
    url(r'(?P<board_id>[0-9]+)/$', views.board, name="board"),
    url(r'^new/$', views.new_board, name="new_board"),
    url(r'^list/new/$', views.new_list, name="new_list"),
    url(r'^list_item/new/$', views.new_list_item, name="new_list_item"),
    url(r'^list_item/change/$', views.change_list_item, name="change_entry"),
    url(r'^member/new/$', views.new_member, name="add_member"),
    url(r'^member/admin/new/$', views.new_admin, name="add_admin"),
    url(r'^member/remove/$', views.remove_member, name="remove_member"),
    url(r'^member/admin/remove/$', views.remove_admin, name="remove_admin"),
    url(r'^$', views.boards, name="boards"),
]
