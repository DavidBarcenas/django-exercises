from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required


def user_data(request):
    return render(request, 'user_data.html')


@login_required
def profile(request):
    return render(request, 'profile.html')
