from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.auth.models import User
from boards.models import Board, List, ListEntry, Comment
from django.http import Http404


@login_required
def boards(request):
    return render(request, 'boards/boards.html',
                  {"created_boards": request.user.get_created_boards(),
                   "other_boards": request.user.get_other_boards()})


@login_required
def board(request, board_id):
    board = get_object_or_404(Board, id=board_id)
    if request.user not in board.members.all():
        return redirect('boards')

    return render(request, 'boards/board.html',
                  {"board": board.get_for_rendering(),
                   "other_boards": request.user.boards.all(),
                   "is_admin": request.user.is_admin(board)})


@login_required
def new_board(request):
    if request.method == 'POST':
        print("SUCCESS!!!!")
    else:
        print("SUCCESS!!!!")
    title = request.POST['board_title']
    board = Board.new(request.user, title)
    return redirect("board", board.id)


@login_required
def delete_board(request):
    board_id = int(request.POST['board_id'])
    board = get_object_or_404(Board, id=board_id)

    if board.creator != request.user:
        raise Http404

    board.delete()

    return redirect("boards")


@login_required
def new_list(request):
    title = request.POST['list_title']
    board_id = int(request.POST['board_id'])

    board = get_object_or_404(Board, id=board_id)
    get_object_or_404(board.members.all(), id=request.user.id)
    basic_list = List.objects.create(title=title, board=board)
    return redirect("board", board.id)


@login_required
def delete_list(request):
    list_id = int(request.POST['list_id'])

    board_list = get_object_or_404(List, id=list_id)
    get_object_or_404(board_list.board.members.all(), id=request.user.id)
    board_list.delete()

    return redirect("board", board_list.board.id)


@login_required
def move_list(request):
    list_id = int(request.POST['list_id'])
    target_board_id = int(request.POST['move_target_id'])

    board_list = get_object_or_404(List, id=list_id)
    get_object_or_404(board_list.board.members.all(), id=request.user.id)
    other_board = get_object_or_404(Board, id=target_board_id)
    get_object_or_404(other_board.members.all(), id=request.user.id)

    board_list.board = other_board
    board_list.save()

    return redirect("board", other_board.id)


@login_required
def new_list_item(request):
    title = request.POST['list_item_title']
    description = request.POST['list_item_description']
    list_id = int(request.POST['list_id'])

    board_list = get_object_or_404(List, id=list_id)
    get_object_or_404(board_list.board.members.all(), id=request.user.id)

    ListEntry.objects.create(title=title,
                             description=description,
                             parent_list=board_list)

    return redirect("board", board_list.board.id)


@login_required
def delete_list_item(request):
    list_entry_id = int(request.POST['list_entry_id'])

    list_entry = get_object_or_404(ListEntry, id=list_entry_id)
    get_object_or_404(list_entry.parent_list.board.members.all(),
                      id=request.user.id)

    list_entry.delete()

    return redirect("board", list_entry.parent_list.board.id)


@login_required
def move_list_item(request):
    list_entry_id = int(request.POST['list_entry_id'])
    target_list_id = int(request.POST['move_target_id'])

    list_entry = get_object_or_404(ListEntry, id=list_entry_id)
    get_object_or_404(list_entry.parent_list.board.members.all(),
                      id=request.user.id)
    other_list = get_object_or_404(List, id=target_list_id)

    list_entry.parent_list = other_list
    list_entry.save()

    return redirect("board", list_entry.parent_list.board.id)


@login_required
def change_list_item(request):
    title = request.POST['list_entry_title']
    description = request.POST['list_entry_description']
    list_id = int(request.POST['list_entry_id'])

    list_entry = get_object_or_404(ListEntry, id=list_id)
    get_object_or_404(list_entry.parent_list.board.members.all(),
                      id=request.user.id)
    list_entry.title = title
    list_entry.description = description
    list_entry.save()

    return redirect("board", list_entry.parent_list.board.id)


@login_required
def post_comment(request):
    comment = request.POST['comment']
    list_id = int(request.POST['list_entry_id'])

    list_entry = get_object_or_404(ListEntry, id=list_id)
    get_object_or_404(list_entry.parent_list.board.members.all(),
                      id=request.user.id)
    comment = Comment(user=request.user, list_entry=list_entry, text=comment)
    comment.save()

    return redirect("board", list_entry.parent_list.board.id)


@login_required
def new_member(request):
    username = request.POST['member_username']
    board_id = int(request.POST['board_id'])

    board = get_object_or_404(Board, id=board_id)
    get_object_or_404(board.admins.all(), id=request.user.id)
    user = get_object_or_404(User, username=username)

    board.members.add(user)
    board.save()

    return redirect("board", board.id)


@login_required
def new_admin(request):
    username = request.POST['member_username']
    board_id = int(request.POST['board_id'])

    board = get_object_or_404(Board, id=board_id)
    get_object_or_404(board.admins.all(), id=request.user.id)
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
    get_object_or_404(board.admins.all(), id=request.user.id)
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
    if user != request.user:
        get_object_or_404(board.admins.all(), id=request.user.id)

    board.members.remove(user)
    board.admins.remove(user)
    board.save()

    return redirect("board", board.id)
