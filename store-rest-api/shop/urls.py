from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),

    path('product/payment/<int:pk>', views.make_pay_paypal, name='payment'),
    path('product/payment/success/<int:pk>',
         views.payment_success, name='success'),
    path('product/payment/cancelled', views.payment_cancelled, name='cancelled'),
    path('product/payed/detail/<int:pk>', views.detail_pay, name='detail_pay'),

    path('product/<int:pk>', views.DetailView.as_view(), name='detail'),
    path('product/<slug:url_clean>', views.DetailView.as_view(), name='detail'),
]
