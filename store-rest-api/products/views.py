from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from comments.models import Comment

from .models import Category, Product, Type
from .serializers import CategorySerializer, CommentSerializer, ProductSerializer, TypeSerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    @action(detail=False, methods=['get'])
    def all(self, request):
        queryset = Product.objects.all()
        serializer = ProductSerializer(queryset, many=True)

        return Response(serializer.data)


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    @action(detail=True, methods=['get'])
    def products(self, request, pk=None):
        queryset = Product.objects.filter(category_id=pk)
        serializer = ProductSerializer(queryset, many=True)

        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def all(self, request):
        queryset = Category.objects.all()
        serializer = CategorySerializer(queryset, many=True)

        return Response(serializer.data)


class TypeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Type.objects.all()
    serializer_class = TypeSerializer

    @action(detail=True, methods=['get'])
    def products(self, request, pk=None):
        queryset = Product.objects.filter(type_id=pk)
        serializer = ProductSerializer(queryset, many=True)

        return Response(serializer.data)

    def all(self, request):
        queryset = Type.objects.all()
        serializer = TypeSerializer(queryset, many=True)

        return Response(serializer.data)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.exclude(product__isnull=True)
    serializer_class = CommentSerializer

    def all(self, request):
        queryset = Comment.objects.all()
        serializer = CommentSerializer(queryset, many=True)

        return Response(serializer.data)
