import pytest
from django_first.models import Payment, City, OrderItem
from django_first.exceptions import PaymentException, StoreException
from django_first.exceptions import LocationException


def test_order_process_ok(db, data):
    (product, customer, store, store_item,
        order, order_item, payment, city, location) = data
    assert order.price == 100
    order.process()
    store_item.refresh_from_db()
    assert order.is_paid is True
    assert store_item.quantity == 90
    assert order.customer.name == 'Alice'
    assert order.customer.user.username == 'alice'


def test_order_item_price_signal_ok(db, data):
    (product, customer, store, store_item,
        order, order_item, payment, city, location) = data
    assert order.price == 100
    OrderItem.objects.create(order=order, product=product, quantity=20)
    assert order.price == 300


def test_order_process_ok_mulitple_payments(db, data):
    (product, customer, store, store_item,
        order, order_item, payment, city, location) = data
    payment.amount = 50
    payment.save()
    Payment.objects.create(
        order=order,
        amount=50,
        is_confirmed=True
    )
    order.process()
    store_item.refresh_from_db()
    assert order.price == 100
    assert order.is_paid is True
    assert store_item.quantity == 90


def test_order_process_fail_not_enough_stock(db, data):
    (product, customer, store, store_item,
        order, order_item, payment, city, location) = data
    order_item.quantity = 200
    order_item.save()
    with pytest.raises(StoreException) as e:
        order.process()
    assert str(e.value) == "Not enough stock"


def test_order_process_fail_not_enough_money(db, data):
    (product, customer, store, store_item,
        order, order_item, payment, city, location) = data
    payment.amount = 10
    payment.save()
    with pytest.raises(PaymentException) as e:
        order.process()
    assert str(e.value) == 'Not enough money'


def test_order_process_fail_payment_not_confirmed(db, data):
    (product, customer, store, store_item, order,
        order_item, payment, city, location) = data
    payment.is_confirmed = False
    payment.save()
    with pytest.raises(PaymentException) as e:
        order.process()
    assert str(e.value) == 'Not enough money'


def test_order_process_fail_location_not_available(db, data):
    (product, customer, store, store_item, order,
        order_item, payment, city, location) = data
    Astana = City.objects.create(
        name='Astana')
    order.city = Astana
    with pytest.raises(LocationException) as e:
        order.process()
    assert str(e.value) == 'Location not available'
