from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

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
    return redirect("boards")
