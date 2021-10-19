from django.db.models import query
from django.db.models.query import QuerySet
from django.shortcuts import render
from rest_framework import viewsets

from .models import Category, Product, Type
from .serializers import CategorySerializer, ProductSerializer, TypeSerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class TypeViewSet(viewsets.ModelViewSet):
    queryset = Type.objects.all()
    serializer_class = TypeSerializer
