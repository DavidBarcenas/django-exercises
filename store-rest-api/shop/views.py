from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, reverse, render
from django.core.paginator import Paginator
from django.views import generic
from paypalcheckoutsdk.core import PayPalHttpClient, SandboxEnvironment
from paypalcheckoutsdk.orders import OrdersCreateRequest, OrdersCaptureRequest
from paypalhttp import HttpError
import environ

from products.models import Category, Product
from shop.models import Payment

env = environ.Env()


def index(req):
    categories = Category.objects.all()

    search = req.GET.get('search')
    category = req.GET.get('category')

    if search:
        products = Product.objects.filter(type=1, title__contains=search)
    else:
        products = Product.objects.filter(type=1)
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

    client_id = env("PAYPAL_CLIENT_ID")
    client_secret = env("PAYPAL_CLIENT_SECRET")
    environment = SandboxEnvironment(
        client_id=client_id, client_secret=client_secret)
    client = PayPalHttpClient(environment)

    order_request = OrdersCreateRequest()
    order_request.prefer('return=representation')
    order_request.request_body({
        "intent": "CAPTURE",
        "purchase_units": [
            {
                "amount": {
                    "currency_code": "USD",
                    "value": "100.00"
                }
            }
        ],
        "application_context": {
            "return_url": "http://localhost:8000/shop/product/payment/success/%s" % product.id,
            "cancel_url": "http://localhost:8000/shop/product/payment/cancelled"
        }
    })

    try:
        response = client.execute(order_request)

        if response.result.status == "CREATED":
            approval_url = str(response.result.links[1].href)
    except IOError as ioe:
        print(ioe)
        if isinstance(ioe, HttpError):
            print(ioe.status_code)

    return render(req, 'payment/buy.html', {'product': product, 'approval_url': approval_url})


@login_required
def payment_success(req, pk):
    product = get_object_or_404(Product, pk=pk)

    client_id = env("PAYPAL_CLIENT_ID")
    client_secret = env("PAYPAL_CLIENT_SECRET")
    environment = SandboxEnvironment(
        client_id=client_id, client_secret=client_secret)
    client = PayPalHttpClient(environment)

    order_id = req.GET.get('token')
    payer_id = req.GET.get('PayerID')

    request = OrdersCaptureRequest(order_id)

    try:
        response = client.execute(request)

        if response:
            paymentModel = Payment.create(
                payment_id=order_id,
                payer_id=payer_id,
                price=product.price,
                user_id=req.user,
                product_id=product,
            )

            paymentModel.save()

            return redirect(reverse('shop:detail_pay', args=[paymentModel.id]))

    except IOError as ioe:
        if isinstance(ioe, HttpError):
            print(ioe.status_code)

    return render(req, 'payment/success.html')


@login_required
def payment_cancelled(req):
    return render(req, 'payment/cancelled.html')


@login_required
def purchased(req):
    return render(req, 'payment/purchased.html', {'payments': Payment.objects.select_related('product').filter(user=req.user)})


@login_required
def detail_pay(req, pk):
    payment = get_object_or_404(Payment, pk=pk)
    return render(req, 'payment/detail.html', {'payment': payment})
