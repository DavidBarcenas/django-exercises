from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('add/', views.add, name='add'),
    path('update/<int:pk>', views.update, name='update'),
    path('contact/', views.contact, name='contact'),
    path('export/', views.export, name='export')
]
