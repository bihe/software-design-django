from typing import List

from .models import Product


class ProductService:

    def get_all_products(self) -> List[Product]:
        products = []
        all_products = Product.objects.all()
        if all_products is None:
            products

        for p in all_products:
            products.append(p)
        return products

    def get_by_id(self, id: int) -> Product:
        try:
            entity = Product.objects.get(id=id)
            return entity
        except Product.DoesNotExist:
            return None

    def get_price(self, product: Product) -> float:
        # in another product app, the logic for getting the price could be different
        return product.price
