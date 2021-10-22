from rest_framework import serializers

from comments.models import Comment

from .models import Product, Category, Type


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class TypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Type
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField()
    type = serializers.StringRelatedField()
    comments = CommentSerializer(read_only=True, many=True)

    class Meta:
        model = Product
        fields = '__all__'
