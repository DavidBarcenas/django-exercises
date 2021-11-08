from django.shortcuts import render
from django.core.paginator import Paginator
from django.views import generic
import paypalrestsdk
import logging
import environ

from products.models import Category, Product

env = environ.Env()


def index(req):
    categories = Category.objects.all()

    search = req.GET.get('search')
    category = req.GET.get('category')

    if search:
        products = Product.objects.filter(title__contains=search)
    else:
        products = Product.objects.all()
        search = ''

    if category:
        products = products .filter(category_id=category)
    else:
        category = ''

    paginator = Paginator(products, 5)
    page_number = req.GET.get('page')
    products_page = paginator.get_page(page_number)

    return render(req, 'store/index.html', {
        'products': products_page,
        'categories': categories,
        'search': search,
        'category': int(category)
    })


class DetailView(generic.DetailView):
    model = Product
    template_name = 'store/detail.html'
    slug_field = 'url_clean'
    slug_url_kwarg = 'url_clean'


def make_pay_paypal(req):
    paypalrestsdk.configure({
        "mode": "sandbox",
        "client_id": env("PAYPAL_CLIENT_ID"),
        "client_secret": env("PAYPAL_CLIENT_SECRET")
    })

    payment = paypalrestsdk.Payment({
        "intent": "sale",
        "payer": {
            "payment_method": "paypal"},
        "redirect_urls": {
            "return_url": "http://localhost:3000/payment/execute",
            "cancel_url": "http://localhost:3000/"},
        "transactions": [{
            "item_list": {
                "items": [{
                    "name": "item",
                    "sku": "item",
                    "price": "5.00",
                    "currency": "USD",
                    "quantity": 1}]},
            "amount": {
                "total": "5.00",
                "currency": "USD"},
            "description": "This is the payment transaction description."}]})

    if payment.create():
        print("Payment created successfully")
    else:
        print(payment.error)

    for link in payment.links:
        if link.rel == "approval_url":
            # Convert to str to avoid Google App Engine Unicode issue
            # https://github.com/paypal/rest-api-sdk-python/pull/58
            approval_url = str(link.href)
            print("Redirect for approval: %s" % (approval_url))
