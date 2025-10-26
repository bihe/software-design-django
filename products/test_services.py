import unittest
from unittest.mock import Mock, patch, MagicMock
from typing import List

from .models import Product
from .services import ProductService, ProductModel


class TestProductModel(unittest.TestCase):
    """Test cases for ProductModel conversion methods."""

    def test_from_product_converts_orm_to_dto(self):
        """Test conversion from Django ORM Product to ProductModel."""
        # Arrange
        product_orm = Mock(spec=Product)
        product_orm.id = 1
        product_orm.name = "Laptop"
        product_orm.description = "Gaming laptop"
        product_orm.price = 999.99

        # Act
        product_model = ProductModel.from_product(product_orm)

        # Assert
        self.assertIsInstance(product_model, ProductModel)
        self.assertEqual(product_model.id, 1)
        self.assertEqual(product_model.name, "Laptop")
        self.assertEqual(product_model.description, "Gaming laptop")
        self.assertEqual(product_model.price, 999.99)

    def test_to_product_creates_new_orm_instance(self):
        """Test conversion from ProductModel to new Django ORM Product."""
        # Arrange
        product_model = ProductModel(
            id=None,
            name="Mouse",
            description="Wireless mouse",
            price=29.99
        )

        # Act
        product_orm = product_model.to_product()

        # Assert
        self.assertIsInstance(product_orm, Product)
        self.assertEqual(product_orm.name, "Mouse")
        self.assertEqual(product_orm.description, "Wireless mouse")
        self.assertEqual(product_orm.price, 29.99)

    def test_to_product_updates_existing_orm_instance(self):
        """Test conversion from ProductModel updates existing Django ORM Product."""
        # Arrange
        existing_product = Mock(spec=Product)
        existing_product.id = 5
        existing_product.name = "Old Name"
        existing_product.description = "Old Description"
        existing_product.price = 100.0

        product_model = ProductModel(
            id=5,
            name="Updated Name",
            description="Updated Description",
            price=150.0
        )

        # Act
        updated_product = product_model.to_product(existing_product)

        # Assert
        self.assertEqual(updated_product.name, "Updated Name")
        self.assertEqual(updated_product.description, "Updated Description")
        self.assertEqual(updated_product.price, 150.0)


class TestProductService(unittest.TestCase):
    """Test cases for ProductService methods."""

    def setUp(self):
        """Set up test fixtures."""
        self.service = ProductService()

    @patch('products.services.Product.objects')
    def test_get_all_products_returns_list_of_product_models(self, mock_objects):
        """Test get_all_products returns list of ProductModel objects."""
        # Arrange
        mock_product1 = Mock(spec=Product)
        mock_product1.id = 1
        mock_product1.name = "Laptop"
        mock_product1.description = "Gaming laptop"
        mock_product1.price = 999.99

        mock_product2 = Mock(spec=Product)
        mock_product2.id = 2
        mock_product2.name = "Mouse"
        mock_product2.description = "Wireless mouse"
        mock_product2.price = 29.99

        mock_objects.all.return_value = [mock_product1, mock_product2]

        # Act
        result = self.service.get_all_products()

        # Assert
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 2)
        self.assertIsInstance(result[0], ProductModel)
        self.assertEqual(result[0].id, 1)
        self.assertEqual(result[0].name, "Laptop")
        self.assertEqual(result[1].id, 2)
        self.assertEqual(result[1].name, "Mouse")
        mock_objects.all.assert_called_once()

    @patch('products.services.Product.objects')
    def test_get_all_products_returns_empty_list_when_no_products(self, mock_objects):
        """Test get_all_products returns empty list when no products exist."""
        # Arrange
        mock_objects.all.return_value = []

        # Act
        result = self.service.get_all_products()

        # Assert
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 0)
        mock_objects.all.assert_called_once()

    @patch('products.services.Product.objects')
    def test_get_by_id_returns_product_model_when_found(self, mock_objects):
        """Test get_by_id returns ProductModel when product exists."""
        # Arrange
        mock_product = Mock(spec=Product)
        mock_product.id = 1
        mock_product.name = "Laptop"
        mock_product.description = "Gaming laptop"
        mock_product.price = 999.99

        mock_objects.get.return_value = mock_product

        # Act
        result = self.service.get_by_id(1)

        # Assert
        self.assertIsInstance(result, ProductModel)
        self.assertEqual(result.id, 1)
        self.assertEqual(result.name, "Laptop")
        self.assertEqual(result.description, "Gaming laptop")
        self.assertEqual(result.price, 999.99)
        mock_objects.get.assert_called_once_with(id=1)

    @patch('products.services.Product.objects')
    def test_get_by_id_returns_none_when_not_found(self, mock_objects):
        """Test get_by_id returns None when product does not exist."""
        # Arrange
        mock_objects.get.side_effect = Product.DoesNotExist()

        # Act
        result = self.service.get_by_id(999)

        # Assert
        self.assertIsNone(result)
        mock_objects.get.assert_called_once_with(id=999)

    def test_get_price_returns_product_price(self):
        """Test get_price returns the price from ProductModel."""
        # Arrange
        product_model = ProductModel(
            id=1,
            name="Laptop",
            description="Gaming laptop",
            price=999.99
        )

        # Act
        result = self.service.get_price(product_model)

        # Assert
        self.assertEqual(result, 999.99)

    def test_get_price_returns_zero_for_product_with_zero_price(self):
        """Test get_price returns 0.0 for product with zero price."""
        # Arrange
        product_model = ProductModel(
            id=1,
            name="Free Sample",
            description="Free product",
            price=0.0
        )

        # Act
        result = self.service.get_price(product_model)

        # Assert
        self.assertEqual(result, 0.0)

    @patch('products.services.Product.objects')
    def test_create_product_saves_and_returns_product_model(self, mock_objects):
        """Test create_product saves to database and returns ProductModel with id."""
        # Arrange
        product_model = ProductModel(
            id=None,
            name="Keyboard",
            description="Mechanical keyboard",
            price=149.99
        )

        mock_saved_product = Mock(spec=Product)
        mock_saved_product.id = 10
        mock_saved_product.name = "Keyboard"
        mock_saved_product.description = "Mechanical keyboard"
        mock_saved_product.price = 149.99
        mock_saved_product.save = Mock()

        # Mock the to_product conversion
        with patch.object(product_model, 'to_product', return_value=mock_saved_product):
            # Act
            result = self.service.create_product(product_model)

        # Assert
        self.assertIsInstance(result, ProductModel)
        self.assertEqual(result.id, 10)
        self.assertEqual(result.name, "Keyboard")
        self.assertEqual(result.description, "Mechanical keyboard")
        self.assertEqual(result.price, 149.99)
        mock_saved_product.save.assert_called_once()

    @patch('products.services.Product.objects')
    def test_update_product_updates_existing_and_returns_product_model(self, mock_objects):
        """Test update_product updates existing product and returns ProductModel."""
        # Arrange
        mock_existing_product = Mock(spec=Product)
        mock_existing_product.id = 5
        mock_existing_product.name = "Old Name"
        mock_existing_product.description = "Old Description"
        mock_existing_product.price = 100.0
        mock_existing_product.save = Mock()

        mock_objects.get.return_value = mock_existing_product

        product_model = ProductModel(
            id=5,
            name="Updated Name",
            description="Updated Description",
            price=150.0
        )

        # Act
        result = self.service.update_product(5, product_model)

        # Assert
        self.assertIsInstance(result, ProductModel)
        self.assertEqual(result.id, 5)
        self.assertEqual(result.name, "Updated Name")
        self.assertEqual(result.description, "Updated Description")
        self.assertEqual(result.price, 150.0)
        mock_objects.get.assert_called_once_with(id=5)
        mock_existing_product.save.assert_called_once()

    @patch('products.services.Product.objects')
    def test_update_product_returns_none_when_not_found(self, mock_objects):
        """Test update_product returns None when product does not exist."""
        # Arrange
        mock_objects.get.side_effect = Product.DoesNotExist()

        product_model = ProductModel(
            id=999,
            name="Updated Name",
            description="Updated Description",
            price=150.0
        )

        # Act
        result = self.service.update_product(999, product_model)

        # Assert
        self.assertIsNone(result)
        mock_objects.get.assert_called_once_with(id=999)

    @patch('products.services.Product.objects')
    def test_delete_product_deletes_and_returns_true(self, mock_objects):
        """Test delete_product deletes product and returns True."""
        # Arrange
        mock_product = Mock(spec=Product)
        mock_product.id = 5
        mock_product.delete = Mock()

        mock_objects.get.return_value = mock_product

        # Act
        result = self.service.delete_product(5)

        # Assert
        self.assertTrue(result)
        mock_objects.get.assert_called_once_with(id=5)
        mock_product.delete.assert_called_once()

    @patch('products.services.Product.objects')
    def test_delete_product_returns_false_when_not_found(self, mock_objects):
        """Test delete_product returns False when product does not exist."""
        # Arrange
        mock_objects.get.side_effect = Product.DoesNotExist()

        # Act
        result = self.service.delete_product(999)

        # Assert
        self.assertFalse(result)
        mock_objects.get.assert_called_once_with(id=999)


if __name__ == '__main__':
    unittest.main()
