from django.test import TestCase
from products.models import Product


class ProductTestCase(TestCase):
    def setUp(self):

        pass

    def test_new_product_saved(self):
        product = Product.objects.create(name="testproduct1", price=19.99, description="testdescription1")
        self.assertEqual(Product.objects.get_by_name("testproduct1") .exists(), True)

    def test_get_products_in_price_range(self):
        p1 = Product.objects.create(name="testproduct1", price=11.99, description="testdescription1")
        p2 = Product.objects.create(name="testproduct2", price=19.99, description="testdescription2")
        p3 = Product.objects.create(name="testproduct3", price=29.99, description="testdescription3")
        p4 = Product.objects.create(name="testproduct4", price=30.00, description="testdescription4")

        expected_products = list([p2, p3])
        # two QuerySets will never be equal, even if they contain the same objects, so we need to convert them to lists
        self.assertEqual(list(Product.objects.get_by_price_range(19.99, 29.99)), expected_products)

