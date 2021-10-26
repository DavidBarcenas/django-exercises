from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm


def user_data(req):
    return render(req, 'user_data.html')


@login_required
def profile(req):
    return render(req, 'profile.html')


def register(req):
    form = UserCreationForm()

    return render(req, 'register.html', {'form': form})
