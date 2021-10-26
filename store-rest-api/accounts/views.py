from django.shortcuts import redirect, render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login

from accounts.forms.custom_user_creation_form import CustomUserCreationForm


def user_data(req):
    return render(req, 'user_data.html')


@login_required
def profile(req):
    return render(req, 'profile.html')


def register(req):
    form = CustomUserCreationForm()

    if req.method == 'POST':
        form = CustomUserCreationForm(data=req.POST)

        if form.is_valid():
            user = form.save()

            if user is not None:
                login(req, user)
                return redirect(reverse('accounts:profile'))

    return render(req, 'register.html', {'form': form})
