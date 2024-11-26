# from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required(login_url="/users/login/")
def homepage(request):
    # return HttpResponse("Hello World! I'm Home.")
    return render(request, 'home.html')

@login_required(login_url="/users/login/")
def about(request):
    # return HttpResponse("My About page.")
    return render(request, 'about.html')
