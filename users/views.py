from django.shortcuts import render, redirect 
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .forms import CustomUserCreationForm, CustomUserChangeForm
# Create your views here.
def register_view(request):
    if request.method == "POST": 
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            login(request, form.save())
            if 'next' in request.POST:
                return redirect(request.POST.get('next'))
            else:
                return redirect("/")
    else:
        form = CustomUserCreationForm()
    return render(request, "users/register.html", { "form": form })

def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            if 'next' in request.POST:
                return redirect(request.POST.get('next'))
            else:
                return redirect("/")
    else: 
        form = AuthenticationForm()
    return render(request, "users/login.html", { "form": form })

@login_required(login_url="/users/login/")
def change_password_view(request, id):
    if int(id) != int(request.user.id):
        messages.error(request, 'Not Permitted URL')
        return redirect("users:settings")
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Successful Update')
            return redirect("users:settings")
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'users/change_password.html', { 'form': form })

@login_required(login_url="/users/login/")
def logout_view(request):
    if request.method == "POST": 
        logout(request) 
        return redirect("users:login")

@login_required(login_url="/users/login/")
def settings_view(request):
    if request.method == "POST":
        form = CustomUserChangeForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Successful Update')
            return redirect("users:settings")
    else:
        form = CustomUserChangeForm(instance=request.user)
    return render(request, "users/settings.html", { "form": form })