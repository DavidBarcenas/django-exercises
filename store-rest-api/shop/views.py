from django.shortcuts import render
from django.core.paginator import Paginator
from django.views import generic

from products.models import Category, Product


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
