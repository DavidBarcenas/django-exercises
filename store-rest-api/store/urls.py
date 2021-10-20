from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(('products.urls', 'products'), namespace='products')),
    path('comments/', include(('comments.urls', 'comments'), namespace='comments')),
]
