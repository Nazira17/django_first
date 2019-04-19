import pytest
from django_first.models import Order, OrderItem, City, Location
from django_first.models import Product, Store, StoreItem, Customer, Payment
from django_first.exceptions import PaymentException, StoreException
from django_first.exceptions import LocationException
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


def test_order_process_ok(db, data):
    (product, customer, store, store_item,
        order, order_item, payment, city, location) = data
    order.process()
    store_item.refresh_from_db()
    assert order.price == 100
    assert order.is_paid is True
    assert store_item.quantity == 90
    assert order.customer.name == 'Alice'
    assert order.customer.user.username == 'alice'


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
