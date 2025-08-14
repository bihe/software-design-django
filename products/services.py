from typing import List

from marshmallow import Schema, fields

from core.services import IProductService
from products.models import Product

# Parallel class representing the Order/OrderPosition entity called *Models. This is a quite common pattern
# to tranfere data between the service and the views. Those objects are called View-Models
# (or Data-Transfer-Objects when you come from Java/C#)
#
# It would not be easy to use the Django model directly in the views, especially when the # model is complex and
# when we do not want to save the object already in the database and working with not yet saved
# objects is not easy in Django (e.g. the id is not yet set, so we cannot use it, cannot access foreign key
# objects, ..) (limitations due to the Active Record pattern in Django ORM)


class ProductModel(Schema):
    id: fields.Integer = fields.Integer(as_string=True)
    name: fields.Str = fields.Str()
    description: fields.Str = fields.Str()
    price: fields.Float = fields.Float()


# this is the concrete implementation of the IProductService
class ProductService(IProductService):

    def get_all_products(self) -> List[ProductModel]:
        products = []
        all_products = Product.objects.all()
        if all_products is None:
            products

        for p in all_products:
            products.append(self._entity_to_model(p))
        return products

    def get_by_id(self, id: int) -> ProductModel:
        try:
            entity = Product.objects.get(id=id)
            return self._entity_to_model(entity)
        except Product.DoesNotExist:
            return None

    def _entity_to_model(self, entity: Product) -> ProductModel:
        if entity is None:
            return None
        model = ProductModel()
        model.id = entity.id
        model.name = entity.name
        model.description = entity.description
        model.price = entity.price
        return model
