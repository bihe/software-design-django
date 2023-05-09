from unittest import TestCase
from unittest.mock import patch
from customers.services import CustomerService

"""
Please note, that we are inheriting from TestCase form the unittest module and not from django.test.TestCase.
This is because we are not testing any Django specific functionality, but only the service class.
"""


class TestCustomerService(TestCase):
    """
    The setUp method is a special method in the TestCase class of the unittest module that is called
    before each test method in the test case.
    Its purpose is to set up any resources or objects that the test methods will need.
    """
    def setUp(self):
        # The patch method takes one or more arguments,
        # which are the objects or functions that you want to replace with mock objects.
        self.mock_class = patch('customers.models.Customer').start()
        # Get the mock instance
        self.mock_instance = self.mock_class.return_value
        # Create an instance of the service class we want to test
        self.customer_service: CustomerService = CustomerService()

    """
    The tearDown method is a special method in the TestCase class of the unittest module that is called
    after each test method in the test case.
    """
    def tearDown(self):
        patch.stopall()

    def test_customer_has_credit(self):
        # Set the credit property of the mock instance
        self.mock_instance.credit = 10
        assert self.customer_service.has_credit(self.mock_instance) == True

    def test_customer_without_credit(self):
        # Set the credit property of the mock instance
        self.mock_instance.credit = 0
        assert self.customer_service.has_credit(self.mock_instance) == False
