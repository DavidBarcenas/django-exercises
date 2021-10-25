from django.shortcuts import render


def user_data(request):
    return render(request, 'user_data.html')
