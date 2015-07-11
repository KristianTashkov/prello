from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.auth.models import User
from boards.models import Board, List, ListEntry


@login_required
def boards(request):
    return render(request, 'boards/boards.html',
                  {"created_boards": request.user.get_created_boards(),
                   "other_boards": request.user.get_other_boards()})


def board(request, board_id):
    board = get_object_or_404(Board, id=board_id)

    return render(request, 'boards/board.html',
                  {"board": board.get_for_rendering()})


@login_required
def new_board(request):
    title = request.POST['board_title']
    board = Board.new(request.user, title)
    return redirect("/boards/" + str(board.id))


@login_required
def new_list(request):
    title = request.POST['list_title']
    board_id = int(request.POST['board_id'])

    board = get_object_or_404(Board, id=board_id)
    basic_list = List.objects.create(title=title, board=board)
    return redirect("board", board.id)


@login_required
def new_list_item(request):
    title = request.POST['list_item_title']
    description = request.POST['list_item_description']
    list_id = int(request.POST['list_id'])

    board_list = get_object_or_404(List, id=list_id)
    ListEntry.objects.create(title=title,
                             description=description,
                             parent_list=board_list)

    return redirect("board", board_list.board.id)


@login_required
def new_member(request):
    username = request.POST['member_username']
    board_id = int(request.POST['board_id'])

    board = get_object_or_404(Board, id=board_id)
    user = get_object_or_404(User, username=username)

    board.members.add(user)
    board.save()

    return redirect("board", board.id)


@login_required
def new_admin(request):
    username = request.POST['member_username']
    board_id = int(request.POST['board_id'])

    board = get_object_or_404(Board, id=board_id)
    user = get_object_or_404(User, username=username)

    board.members.add(user)
    board.admins.add(user)
    board.save()

    return redirect("board", board.id)


@login_required
def remove_admin(request):
    user_id = int(request.POST['user_id'])
    board_id = int(request.POST['board_id'])

    board = get_object_or_404(Board, id=board_id)
    user = get_object_or_404(User, id=user_id)

    board.admins.remove(user)
    board.save()

    return redirect("board", board.id)


@login_required
def remove_member(request):
    user_id = int(request.POST['user_id'])
    board_id = int(request.POST['board_id'])

    board = get_object_or_404(Board, id=board_id)
    user = get_object_or_404(User, id=user_id)

    board.members.remove(user)
    board.admins.remove(user)
    board.save()

    return redirect("board", board.id)
