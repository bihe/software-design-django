import unittest
from unittest.mock import Mock, patch

from core.serializers import CustomerSerializer, ProductSerializer
from orders.services import OrderModel, OrderPositionModel, OrderService


class TestOrderService(unittest.TestCase):
    """
    The setUp method is a special method in the TestCase class of the unittest module that is called
    before each test method in the test case.
    Its purpose is to set up any resources or objects that the test methods will need.
    """

    def setUp(self):
        # create a mock instance of customer_service and product_service
        self.customer_service = Mock()
        self.product_service = Mock()
        # create a real OrderService instance and provide the mock instances
        self.order_service = OrderService(product_service=self.product_service, customer_service=self.customer_service)

        product_schema = ProductSerializer()
        customer_schema = CustomerSerializer()

        # Sample data for order creation > OrderModel
        order_positions: list[OrderPositionModel] = []
        order_position1 = OrderPositionModel()
        order_position1.pos = 1
        order_position1.quantity = 2
        order_position1.price = 10
        order_position1.product = product_schema.load({"id": "1", "name": "product1"})
        order_positions.append(order_position1)

        order_position2 = OrderPositionModel()
        order_position2.pos = 2
        order_position2.quantity = 3
        order_position2.price = 15
        order_position2.product = product_schema.load({"id": "2", "name": "product2"})
        order_positions.append(order_position2)

        order_model = OrderModel()
        order_model.order_positions = order_positions
        order_model.total_price = 65.0
        order_model.customer = customer_schema.load({"username": "testuser"})

        self.data: OrderModel = order_model

    def test_create_order_customer_has_credit(self):
        with (
            patch("orders.services.Order"),
            patch("orders.services.OrderPosition"),
        ):
            # Set the redeem_credit method of the mock instance to return True
            self.customer_service.redeem_credit.return_value = True
            order_id = self.order_service.create_order(self.data)
            assert order_id is not None  # assert that the order is not None
            assert self.customer_service.redeem_credit.called  # assert that the redeem_credit method was called

    def test_create_order_customer_without_credit(self):
        with (
            patch("orders.services.Order"),
            patch("orders.services.OrderPosition"),
        ):
            # Set the redeem_credit method of the mock instance to return True
            self.customer_service.redeem_credit.return_value = False
            with self.assertRaises(Exception):
                self.order_service.create_order(self.data)
            assert self.customer_service.redeem_credit.called
