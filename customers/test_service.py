from unittest import TestCase
from unittest.mock import patch
from customers.services import CustomerService


class TestCustomerService(TestCase):

    def setUp(self):
        self.mock_class = patch('customers.models.Customer').start()
        self.mock_instance = self.mock_class.return_value
        self.customer_service: CustomerService = CustomerService()

    def tearDown(self):
        patch.stopall()

    def test_customer_has_credit(self):
        self.mock_instance.credit = 10
        assert self.customer_service.has_credit(self.mock_instance) == True

    def test_customer_without_credit(self):
        self.mock_instance.credit = 0
        assert self.customer_service.has_credit(self.mock_instance) == False


"""
class TestCustomerService(TestCase):

    @patch('customers.models.Customer')
    def test_customer_has_credit(mock_class):
        customer_service: CustomerService = CustomerService()
        mock_instance = mock_class.return_value
        mock_instance.credit = 10
        assert customer_service.has_credit(mock_instance) == True
        pass


    @patch('customers.models.Customer')
    def test_customer_without_credit(mock_class):
        customer_service: CustomerService = CustomerService()
        mock_instance = mock_class.return_value
        mock_instance.credit = 0
        assert customer_service.has_credit(mock_instance) == False
         pass
"""

"""
class ProductTestCase(TestCase):

    def setUp(self):
        self.customer_service = CustomerService()
        pass

   # TODO: why does this not work?
    @mock_model('customers.models.Customer', specs={'credit': 10})
    def test_my_test(self):
        customer = Customer.objects.create(username="testuser", password="testpassword", credit=0)
        #customer = Customer(username="testuser", password="testpassword", credit=1)
        self.assertTrue(self.customer_service.has_credit(customer))
"""
