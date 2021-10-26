from django.shortcuts import redirect, render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login


def user_data(req):
    return render(req, 'user_data.html')


@login_required
def profile(req):
    return render(req, 'profile.html')


def register(req):
    form = UserCreationForm()

    if req.method == 'POST':
        form = UserCreationForm(data=req.POST)

        if form.is_valid():
            user = form.save()

            if user is not None:
                login(req, user)
                return redirect(reverse('accounts:profile'))

    return render(req, 'register.html', {'form': form})
