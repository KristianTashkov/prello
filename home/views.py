from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout

# Create your views here.

def index(request):
	return render(request, 'home/register.html');

def login_request(request):
    username = request.POST['login_username']
    password = request.POST['login_password']
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            return redirect("boards")
    else:
        return render(request, 'home/register.html', { 'error_message': "Invalid login details"})

def logout_request(request):
    logout(request)
    return redirect('/')