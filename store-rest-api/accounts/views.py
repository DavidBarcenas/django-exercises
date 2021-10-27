from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect, render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login

from accounts.forms import CustomUserCreationForm, UserProfileForm
from accounts.models import UserProfile


def user_data(req):
    return render(req, 'user_data.html')


@login_required
def profile(req):
    form = UserProfileForm()

    if req.method == 'POST':
        try:
            user_profile = UserProfile.objects.get(user=req.user)
            form = UserProfileForm(req.POST, req.FILES, instance=user_profile)
        except ObjectDoesNotExist:
            form = UserProfileForm(req.POST, req.FILES)

        if form.is_valid():
            user_profile = form.save(commit=False)
            user_profile.user = req.user
            user_profile.save()

    return render(req, 'profile.html', {'form': form})


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
