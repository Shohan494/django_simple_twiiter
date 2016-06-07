# Create your views here.
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.contrib.auth import login, logout

from django.contrib.auth.forms import UserCreationForm, AuthenticationForm


def sign_up(request):
    form = UserCreationForm()
    return render(request, 'user/sign/up.html', {'form': form})


def sign_up_process(request):
    new_user_form = UserCreationForm(request.POST or None)
    if new_user_form.is_valid():
        new_user_form.save()
        return redirect(reverse('sign_up_success'))
    return render(request, 'user/sign/up.html', {'form': new_user_form})


def sign_up_success(request):
    return render(request, 'user/sign/up_success.html')


def sign_in(request):
    form = AuthenticationForm()
    return render(request, 'user/sign/in.html', {'form': form})


def sign_in_process(request):
    form = AuthenticationForm(data=request.POST or None)
    if form.is_valid():
        login(request, form.get_user())
        return redirect('/')
    return render(request, 'user/sign/in.html', {'form': form})


def log_out(request):
    logout(request)
    return redirect('/')
