from django.urls import include, path
from rest_framework import routers

from .views import CategoryViewSet, CommentViewSet, ProductViewSet, TypeViewSet

router = routers.SimpleRouter()
router.register('products', ProductViewSet)
router.register('category', CategoryViewSet)
router.register('type', TypeViewSet)
router.register('comment', CommentViewSet)

urlpatterns = [
    path('', include(router.urls))
]
