from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from boards.models import Board, List, ListEntry

# Create your views here.


def index(request):
    if request.user.is_active:
        return redirect("boards")
    return render(request, 'home/register.html')


def login_request(request):
    username = request.POST['login_username']
    password = request.POST['login_password']
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            return redirect("boards")
    else:
        return render(request, 'home/register.html',
                      {'error_message': "Invalid login details"})


def logout_request(request):
    logout(request)
    return redirect('/')


def register_request(request):
    username = request.POST['username']
    email = request.POST['username']
    password1 = request.POST['password1']
    password2 = request.POST['password2']

    user, new = User.objects.get_or_create(username=username)
    if not new:
        return render(request, 'home/register.html',
                      {'error_message': "Username already exists"})

    if password1 != password2:
        return render(request, 'home/register.html',
                      {'error_message':
                       "Passwords don't match, please try again."})

    user.email = email
    user.set_password(password1)
    user.save()
    user = authenticate(username=username, password=password1)
    login(request, user)
    create_default_boards(user)

    return redirect("boards")


def create_default_boards(user):
    board = Board(title="Welcome")
    board.save()
    board.admins.add(user)
    board.members.add(user)

    basic_list = List.objects.create(title="Basic", board=board)
    advanced_list = List.objects.create(title="Advanced", board=board)

    ListEntry.objects.create(title="Add new list items to this list",
                             description="You can add new list items to any\
                             list by pressing the \"Add new lists\" button",
                             parent_list=basic_list)

    ListEntry.objects.create(title="Add members to a list item",
                             description="You can add members to a list item.\
                                          Try it!",
                             parent_list=basic_list)

    ListEntry.objects.create(title="Create a new list",
                             description="You can create new lists in this\
                                          board. Try it!",
                             parent_list=advanced_list)
