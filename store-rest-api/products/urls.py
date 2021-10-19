from django.urls import include, path
from rest_framework import routers

from .views import ProductViewSet

router = routers.SimpleRouter()
router.register('products', ProductViewSet)

urlpatterns = [
    path('', include(router.urls))
]
