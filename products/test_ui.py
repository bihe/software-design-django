from unittest.mock import MagicMock

from dependency_injector import containers, providers
from django.urls import reverse
from django.test import TestCase

from core.models import Product
from core.services import IProductService


class TestContainer(containers.DeclarativeContainer):
    product_factory = providers.Factory(
        MagicMock,
        spec=Product
    )

    product_service = providers.Singleton(
        MagicMock,
        spec=IProductService
    )


class IndexTests(TestCase):

    def setUp(self):
        self.mock_product_list = [
            TestContainer.product_factory(id=1, name="testproduct1", description="testdescription1"),
            TestContainer.product_factory(id=2, name="testproduct2", description="testdescription2"),
        ]
        c = TestContainer()
        c.product_service().get_all_products.return_value = self.mock_product_list
        c.wire(modules=["products.views", ])

    def test_index(self):
        response = self.client.get(reverse("index"))

        self.assertIn('products_list', response.context)
        self.assertEqual(list(response.context['products_list']), self.mock_product_list)
