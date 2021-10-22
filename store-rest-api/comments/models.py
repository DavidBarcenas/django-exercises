from django.db import models

from products.models import Product


class Comment(models.Model):
    text = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)

    def __str__(self) -> str:
        return 'Comment #{}'.format(self.id)


class Contact(models.Model):
    name = models.CharField(max_length=255)
    lastname = models.CharField(max_length=255)
    email = models.CharField(max_length=70)
    phone = models.CharField(max_length=15)
    date = models.DateField()
    document = models.FileField(upload_to='uploads/contact')


class TypeContact(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.name
