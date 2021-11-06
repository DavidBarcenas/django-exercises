from django.shortcuts import render
from django.core.paginator import Paginator

from products.models import Product


def index(req):
    products = Product.objects.all()

    paginator = Paginator(products, 5)
    page_number = req.GET.get('page')
    products_page = paginator.get_page(page_number)

    return render(req, 'store/index.html', {'products': products_page})
