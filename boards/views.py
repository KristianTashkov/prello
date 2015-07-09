from django.shortcuts import render
from django.contrib.auth import logout

# Create your views here.

def boards(request):
	return render(request, 'boards/boards.html');
