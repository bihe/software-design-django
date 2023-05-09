from typing import List

from core.services import IProductService
from products.models import Product


class ProductService(IProductService):

    def get_all_products(self) -> List[Product]:
        return Product.objects.all()

    def get_price(self, product: Product) -> float:
        return 1.0
