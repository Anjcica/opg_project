from django.db import models
from user.models import User


class Opg(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, unique=True, blank=False)
    address = models.CharField(max_length=50, blank=True)
    phone = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return self.name


class ProductCategory(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=50, blank=False, null=False)
    category = models.ForeignKey(ProductCategory, on_delete=models.SET(None), blank=True, null=True)
    opg = models.ForeignKey(Opg, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
