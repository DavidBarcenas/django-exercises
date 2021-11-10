from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render
from django.core.paginator import Paginator
from django.views import generic
import paypalrestsdk
import logging
import environ

from products.models import Category, Product
from shop.models import Payment

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
        category = int(category)
    else:
        category = ''

    paginator = Paginator(products, 5)
    page_number = req.GET.get('page')
    products_page = paginator.get_page(page_number)

    return render(req, 'store/index.html', {
        'products': products_page,
        'categories': categories,
        'search': search,
        'category': category
    })


class DetailView(generic.DetailView):
    model = Product
    template_name = 'store/detail.html'
    slug_field = 'url_clean'
    slug_url_kwarg = 'url_clean'


@login_required
def make_pay_paypal(req, pk):
    product = get_object_or_404(Product, pk=pk)

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
            "return_url": "http://localhost:8000/shop/product/payment/success/%s" % product.id,
            "cancel_url": "http://localhost:8000/shop/product/payment/cancelled"},
        "transactions": [{
            "item_list": {
                "items": [{
                    "name": "item",
                    "sku": "item",
                    "price": "12.00",
                    "currency": "USD",
                    "quantity": 1}]},
            "amount": {
                "total": "12.00",
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

    return render(req, 'payment/buy.html', {'product': product, 'approval_url': approval_url})


@login_required
def payment_success(req, pk):
    product = get_object_or_404(Product, pk=pk)

    payment_id = req.GET.get('paymentId')
    payer_id = req.GET.get('PayerID')

    payment = paypalrestsdk.Payment.find(payment_id)

    try:
        if payment.execute({'payer_id': payer_id}):
            paymentModel = Payment(
                payment_id=payment_id,
                payer_id=payer_id,
                price=product.price,
                user_id=req.user,
                product_id=product,
            )
            paymentModel.save()
        else:
            print()
    except paypalrestsdk.exceptions.ResourceNotFound:
        print('An ocurred error')

    return render(req, 'payment/success.html')


@login_required
def payment_cancelled(req):
    return render(req, 'payment/cancelled.html')
