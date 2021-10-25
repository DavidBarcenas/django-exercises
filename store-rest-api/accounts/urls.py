from django.urls import path

from . import views

urlpatterns = [
    path('user_data/', views.user_data)
]
