from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=100)


class Store(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='stores'
    )
    quantity = models.IntegerField()
    location = models.CharField(max_length=100, blank=True)


class Customer(models.Model):
    name = models.CharField(max_length=100)


class Cart(models.Model):
    customer = models.ForeignKey(
        Customer,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='names'
    )
    cart = models.IntegerField()
