import datetime

from django.test import TestCase

from customers.models import Customer
from products.models import Product

from .models import Order, OrderPosition


class TestOrders(TestCase):
    def setUp(self) -> None:
        pass

    def test_create_order(self) -> None:
        user = Customer()
        user.save()

        self.assertIsNotNone(user.id)

        order = Order()
        order.total_price = 1
        order.order_date = datetime.datetime.now()
        order.user = user
        order.save()

        self.assertIsNotNone(order.id)

        product = Product()
        product.description = "test"
        product.price = 1.0
        product.name = "testproduct"

        product.save()

        self.assertIsNotNone(product.id)

        # create the order positions
        order_pos = OrderPosition()
        order_pos.pos = 1
        order_pos.quantity = 1
        order_pos.price = 1.0
        # reference the created order
        order_pos.order = order
        order_pos.product = product

        order_pos.save()

        saved_order = Order.objects.get_by_id(order.id)

        # check the references
        self.assertIsNotNone(saved_order)
        self.assertEqual(order.id, saved_order.id)

        positions = Order.objects.get_order_positions(order.id)
        self.assertIsNotNone(positions)
        self.assertTrue(len(positions) == 1)
        self.assertEqual(1, positions[0].pos)
        self.assertEqual("testproduct", positions[0].product.name)
