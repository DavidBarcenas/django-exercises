from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('product/payment', views.make_pay_paypal, name='payment'),
    path('product/<int:pk>', views.DetailView.as_view(), name='detail'),
    path('product/<slug:url_clean>', views.DetailView.as_view(), name='detail'),
]
