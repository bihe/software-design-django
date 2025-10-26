from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

from dependency_injector.wiring import Provide
from django.db import transaction

from customers.models import Customer
from customers.services import CustomerModel, CustomerService
from products.services import ProductModel, ProductService

from .logging import logger
from .models import Order, OrderPosition

# Parallel class representing the Order/OrderPosition entity called *Models. This is a quite common pattern
# to tranfere data between the service and the views. Those objects are called View-Models
# (or Data-Transfer-Objects when you come from Java/C#)
#
# It would not be easy to use the Django model directly in the views, especially when the # model is complex and
# when we do not want to save the object already in the database and working with not yet saved
# objects is not easy in Django (e.g. the id is not yet set, so we cannot use it, cannot access foreign key
# objects, ..) (limitations due to the Active Record pattern in Django ORM)


@dataclass
class OrderPositionModel:
    pos: int = 0
    quantity: int = 0
    price: float = 0.0
    product: ProductModel = None


@dataclass
class OrderModel:
    # customer: fields.Nested = fields.Nested(CustomerSerializer)

    id: Optional[int] = None
    order_number: str = ""
    total_price: float = 0.0
    order_positions: list[OrderPositionModel] = field(default_factory=list)
    customer: CustomerModel = None
    order_date: datetime.date = None


class OrderService:
    def __init__(
        self,
        product_service: ProductService = Provide("product_service"),
        customer_service: CustomerService = Provide("customer_service"),
    ):
        logger.debug(f"OrderService.__init__(product_service: {product_service}, customer_service: {customer_service}")
        self.product_service = product_service
        self.customer_service = customer_service

    def get_order_model(self, customer: Customer, product_list: list[ProductModel]) -> OrderModel:
        order: OrderModel = OrderModel()
        order.customer = customer
        order_positions: list[OrderPositionModel] = []  # List to store the order positions
        product_pos_map: dict[int, ProductModel] = {}  # Map to store the product id and position in the order
        pos: int = 0
        total_price: float = 0.0
        for product_id in product_list:
            if product_id in product_pos_map:
                orderpos: OrderPositionModel = order_positions[product_pos_map[product_id]]
                orderpos.quantity += 1
                total_price += self.product_service.get_price(self.product_service.get_by_id(product_id))
            else:
                product: ProductModel = self.product_service.get_by_id(product_id)
                if product is None:
                    continue
                pos += 1
                product_pos_map[product_id] = pos - 1
                orderpos: OrderPositionModel = OrderPositionModel()
                orderpos.pos = pos
                orderpos.product = product
                orderpos.quantity = 1
                orderpos.price = self.product_service.get_price(product)
                total_price += orderpos.price
                order_positions.append(orderpos)  # Add the order position to the list

        order.order_positions = order_positions
        order.total_price = total_price

        return order

    def create_order(self, order: OrderModel) -> Optional[int]:
        logger.debug(f"OrderService.create_order(order: {order})")

        with transaction.atomic():
            order_positions = order.order_positions
            customer = self.customer_service.get_by_username(order.customer.username)

            # we need a customer to carry on
            if customer is None:
                raise Exception(
                    f"cannot create order without customer, no customer for username '{order.customer.username}'"
                )

            # do a check on the customer credit
            # if the customer can afford the order
            if not self.customer_service.redeem_credit(customer, order.total_price):
                raise Exception(
                    (
                        f"cannot perform order without enough credit, total order price of [{order.total_price}] "
                        f"is higher than credit of [{customer.credit}]"
                    )
                )

            order_to_save = Order()
            customer_entity = self.customer_service.model_to_entity(customer)
            order_to_save.user = customer_entity
            order_to_save.total_price = order.total_price
            order_to_save.order_date = datetime.now()
            order_to_save.save()

            for order_position in order_positions:
                p: OrderPositionModel = order_position
                product_id = p.product.id
                product = self.product_service.get_by_id(product_id)

                order_position_to_save = OrderPosition()
                order_position_to_save.order = order_to_save
                order_position_to_save.pos = p.pos
                product_entity = self.product_service.model_to_entity(product)
                order_position_to_save.product = product_entity
                order_position_to_save.quantity = p.quantity
                order_position_to_save.price = p.price

                order_position_to_save.save()

            return order_to_save.id

    def get_order(self, order_id: int) -> OrderModel:
        try:
            entity = Order.objects.get(id=order_id)
            order_model = self._entity_to_model(entity)
            return order_model
        except Order.DoesNotExist:
            return None

    def get_orders(self, username: str) -> list[OrderModel]:
        try:
            orders = Order.objects.filter(user__username=username).order_by("-id", "-order_date")
            order_list: list[OrderModel] = []
            for entity in orders:
                order_model = self._entity_to_model(entity)
                order_list.append(order_model)
            return order_list
        except Order.DoesNotExist:
            return None

    def _entity_to_model(self, entity: Order) -> OrderModel:
        order_model = OrderModel()
        order_model.order_number = entity.id
        order_model.total_price = entity.total_price
        order_model.customer = entity.user
        order_model.order_positions = []
        order_model.order_date = entity.order_date
        for p in entity.order_positions.all():
            order_position = OrderPositionModel()
            order_position.pos = p.pos
            order_position.quantity = p.quantity
            order_position.price = p.price
            order_position.product = p.product
            order_model.order_positions.append(order_position)
        return order_model
