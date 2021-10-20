from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Category, Product, Type
from .serializers import CategorySerializer, ProductSerializer, TypeSerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    @action(detail=True, methods=['get'])
    def products(self, request, pk=None):
        queryset = Product.objects.filter(category_id=pk)
        serializer = ProductSerializer(queryset, many=True)

        return Response(serializer.data)


class TypeViewSet(viewsets.ModelViewSet):
    queryset = Type.objects.all()
    serializer_class = TypeSerializer

    @action(detail=True, methods=['get'])
    def products(self, request, pk=None):
        queryset = Product.objects.filter(type_id=pk)
        serializer = ProductSerializer(queryset, many=True)

        return Response(serializer.data)
