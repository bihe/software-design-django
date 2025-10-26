from dataclasses import dataclass
from typing import List, Optional

from django.db import models

from .models import Product


@dataclass
class ProductModel:
    """The ProductService uses own models and converts the persistence models."""

    id: Optional[int] = None
    name: str = ""
    description: str = ""
    price: float = 0.0

    @classmethod
    def from_product(cls, product: Product) -> "ProductModel":
        """
        Convert a database Product model to a ProductModel.

        Args:
            product: The Product ORM instance

        Returns:
            A ProductModel instance
        """
        return cls(id=product.id, name=product.name, description=product.description, price=product.price)

    def to_product(self, product_instance: Product = None) -> Product:
        """
        Convert this ProductModel to a database Product model.

        Args:
            product_instance: Optional existing Product instance to update

        Returns:
            A Product ORM instance (not saved to database)
        """
        if product_instance is None:
            product_instance = Product()

        product_instance.name = self.name
        product_instance.description = self.description
        product_instance.price = self.price

        return product_instance


class ProductService:

    def get_all_products(self) -> List[ProductModel]:
        """
        Get all products as ProductModel objects.

        Returns:
            List of ProductModel objects
        """
        products = []
        all_products = Product.objects.all()

        for p in all_products:
            products.append(ProductModel.from_product(p))
        return products

    def get_by_id(self, id: int) -> Optional[ProductModel]:
        """
        Get a product by ID as a ProductModel.

        Args:
            id: The product ID

        Returns:
            ProductModel object or None if not found
        """
        try:
            entity = Product.objects.get(id=id)
            return ProductModel.from_product(entity)
        except Product.DoesNotExist:
            return None

    def get_price(self, product_model: ProductModel) -> float:
        """
        Get the price from a ProductModel.

        Args:
            product_model: ProductModel object

        Returns:
            The product price
        """
        # in another product app, the logic for getting the price could be different
        return product_model.price

    def create_product(self, product_model: ProductModel) -> ProductModel:
        """
        Create a new product from ProductModel.

        Args:
            product_model: ProductModel object with product data

        Returns:
            Created ProductModel with id
        """
        product_entity = product_model.to_product()
        product_entity.save()
        return ProductModel.from_product(product_entity)

    def update_product(self, id: int, product_model: ProductModel) -> Optional[ProductModel]:
        """
        Update an existing product.

        Args:
            id: The product ID to update
            product_model: ProductModel object with updated data

        Returns:
            Updated ProductModel or None if not found
        """
        try:
            existing_product = Product.objects.get(id=id)
            updated_product = product_model.to_product(existing_product)
            updated_product.save()
            return ProductModel.from_product(updated_product)
        except Product.DoesNotExist:
            return None

    def delete_product(self, id: int) -> bool:
        """
        Delete a product by ID.

        Args:
            id: The product ID to delete

        Returns:
            True if deleted, False if not found
        """
        try:
            product = Product.objects.get(id=id)
            product.delete()
            return True
        except Product.DoesNotExist:
            return False

    def model_to_entity(self, product: ProductModel) -> models.QuerySet:
        try:
            return Product.objects.get(id=product.id)
        except Product.DoesNotExist:
            return None
