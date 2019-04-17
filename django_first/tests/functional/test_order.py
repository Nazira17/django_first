import pytest
from django_first.models import Order, OrderItem
from django_first.models import Product, Store, StoreItem, Customer


@pytest.fixture
def data():
    product = Product.objects.create(
        name='apple',
        price=10
    )
    customer = Customer.objects.create(
        name='Alice'
    )
    store = Store.objects.create(
        location='Almaty',
    )
    store_item = StoreItem.objects.create(
        store=store,
        product=product,
        quantity=100
    )
    order = Order.objects.create(
        location='Almaty',
        customer=customer
    )
    order_item = OrderItem.objects.create(
        order=order,
        product=product,
        quantity=10
    )
    return product, customer, store, store_item, order, order_item


def test_order_process(db, data):
    product, customer, store, store_item, order, order_item = data
    order.process()
    store_item.refresh_from_db()
    assert order.price == 100
    assert order.is_paid is True
    assert store_item.quantity == 90
    assert order.customer.name == 'Alice'
