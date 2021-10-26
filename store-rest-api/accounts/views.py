from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required


def user_data(request):
    if request.user.is_authenticated:
        return render(request, 'user_data.html')
    else:
        return redirect('/accounts/login/')


@login_required
def profile(request):
    return render(request, 'profile.html')
