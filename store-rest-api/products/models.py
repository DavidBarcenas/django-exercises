from django.db import models


class Category(models.Model):
    title = models.CharField(max_length=255)
    url_clean = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.title


class Type(models.Model):
    title = models.CharField(max_length=255)
    url_clean = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.title


class Product(models.Model):
    title = models.CharField(max_length=255)
    url_clean = models.CharField(max_length=255)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    type = models.ForeignKey(Type, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.title
