import datetime
from django.test import TestCase
from core.models import (Customer, Product,
                        Adress, Workplace)

from decimal import Decimal




class TestProduct(TestCase):
    owner = Customer(first_name="Adam", last_name="Tete", dob=datetime.date.today())

    product_properties = {
        'global_interest_rate_dec' : Decimal('5.25'),
        'lombard_rate_dec' : Decimal('6.50'),
        'product_name' : 'L1',
        'amount_requested' : 10000,
        'loan_period': 12,
        'created_date': datetime.date.today(),
        'owner' : owner
    }

    def setUp(self):
        
        self.product = Product(**self.product_properties)

    # def tearDown(self) -> None:
        '''
        to jest po to zeby przywrocic rzeczy, jesli robilbym cos poza baza danych
        '''
    #     return super().tearDown()

    def test_product_creation(self):
        self.owner.save()
        self.product.save()
        self.assertIsNotNone(self.product.id)
        self.assertIsNotNone(self.product.owner)
        print(self.product.amount_requested)