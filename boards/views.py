from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from boards.models import Board


@login_required
def boards(request):
    return render(request, 'boards/boards.html',
                  {"created_boards": request.user.get_created_boards(),
                   "other_boards": request.user.get_other_boards()})


def board(request, board_id):
    return render(request, 'boards/board.html',
                  {"id": board_id})


@login_required
def new_board(request):
    title = request.POST['board_title']
    board = Board.new(request.user, title)
    return redirect("/boards/" + str(board.id))
