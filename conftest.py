import pytest
from django_first.models import (
    Product, Store, StoreItem, Customer, Payment,
    Order, OrderItem, City, Location)
from django.contrib.auth.models import User


@pytest.fixture
def data():
    product = Product.objects.create(
        name='apple',
        price=10
    )
    city = City.objects.create(
        name='Almaty'
    )
    location = Location.objects.create(
        city=city,
        address='Abay str'
    )
    user = User.objects.create_user(
        username='alice',
        password='alice'
    )
    customer = Customer.objects.create(
        name='Alice',
        user=user
    )
    store = Store.objects.create(
        location=location
    )
    store_item = StoreItem.objects.create(
        store=store,
        product=product,
        quantity=100
    )
    order = Order.objects.create(
        city=city,
        customer=customer
    )
    order_item = OrderItem.objects.create(
        order=order,
        product=product,
        quantity=10
    )
    payment = Payment.objects.create(
        order=order,
        amount=1000,
        is_confirmed=True
    )
    return (product, customer, store, store_item,
            order, order_item, payment, city, location)
