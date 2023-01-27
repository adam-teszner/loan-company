# import faker
from django.core.management.base import BaseCommand
from core.models import *

from .examples import first_names, last_names


class Command(BaseCommand):
    help = 'Populating db with fake data'


    def handle(self, *args, **kwargs):
        print(first_names)
