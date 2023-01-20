from django.test import TestCase
from rest_framework.test import APIRequestFactory


factory = APIRequestFactory()
request = factory.get('/search/q/', {'first_name': 'Cain'}, format='datatables')