from typing import List

from core.services import IProductService
from products.models import Product


# this is the concrete implementation of the IProductService
class ProductService(IProductService):

    def get_all_products(self) -> List[Product]:
        return Product.objects.all()

    def get_price(self, product: Product) -> float:
        # in another product app, the logic for getting the price could be different
        return product.price
