import time as t
from django.core.management.base import BaseCommand
from core.models import Product, Payment


class Command(BaseCommand):
    help = 'Updates database with current debt and delay'
    start = t.time()



    def launch_methods(self, object):
        # object.debt()
        object.opti_debt(object.tot_paid, object.complete)
        # object.delay()
        object.opti_delay(object.tot_paid)
        object.save()

    def handle(self, *args, **kwargs):


        products = Product.objects.all()
        [self.launch_methods(prod) for prod in products]

        end = t.time()

        print('done in:', end-self.start, 'sec')
