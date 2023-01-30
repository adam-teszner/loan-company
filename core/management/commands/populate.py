import datetime
import time as t
import random
from pprint import pprint
from faker import Faker
from decimal import Decimal
from django.core.management.base import BaseCommand
from core.models import Product, Payment, Customer, Adress, Workplace

# from .examples import first_names, last_names

f = Faker()
f_pl = Faker('pl_PL')

class Command(BaseCommand):
    help = 'Populates database with fake data, pass in 4 arguments (type:int)'

    def add_arguments(self, parser):
        parser.add_argument('customers', help='number of customers with adresses, workplaces, defaults to 10', type=int, default=10)
        parser.add_argument('products', help='number of products, defaults to 15', type=int, default=15)
        parser.add_argument('payments', help='number of payments, defaults to 30', type=int, default=30)
        parser.add_argument('user_id', help='User ID associated with created data', type=int, default=4)
    
    def handle(self, *args, **kwargs):
        start = t.time()
        obj_count = 0
        customer_ids = []
        product_ids = []

        c = kwargs['customers']
        p = kwargs['products']
        pm = kwargs['payments']
        user_id = kwargs['user_id']

        for obj in range(c):
            customer_params = {
                # 'adress_id': None,
                'created_by_id': user_id,
                'created_date': datetime.date.today(),
                'dob': f.date_of_birth(minimum_age=18, maximum_age=70),
                'email': f.ascii_email(),
                'esd': f.date_between(start_date='-48y', end_date='-18y'),
                'first_name': f.first_name(),
                'gender': 'm',
                # 'id': None,
                'id_passport': f_pl.unique.identity_card_number(),
                'last_name': f.last_name(),
                'martial_status': 'mr',
                'phone_no': f.unique.random_number(digits=9),
                'position': f.job()[:40]+'...',
                'salaty': f.random_number(digits=4),
                'social_security_no_pesel': f_pl.unique.pesel(),
                'work_status': 'ft',
                # 'workplace_id': None
                }

            workplace_params = {
                # 'adress_id': None,
                'email': f.ascii_email(),
                # 'id': None,
                'id_nip': f_pl.unique.nip(),
                'name': f.company(),
                'phone_no': f.unique.random_number(digits=9),
                }

            adress_params = {
                'building_no': f.building_number(),
                'city': f.city(),
                # 'id': None,
                'street': f.street_name(),
                'zip_code': f_pl.zipcode(),
                }
            work_adress_params = {
                'building_no': f.building_number(),
                'city': f.city(),
                # 'id': None,
                'street': f.street_name(),
                'zip_code': f_pl.zipcode(),
                }
            obj = Customer(**customer_params)
            obj.adress = Adress(**adress_params)
            obj.workplace = Workplace(**workplace_params)
            obj.workplace.adress = Adress(**work_adress_params)


            objects = [
                obj.workplace.adress,
                obj.workplace,
                obj.adress,
                obj,
            ]
            [o.save() for o in objects]
            customer_ids.append(obj.id)
            obj_count += 4
            
        for prod in range(p):
            product_params = {
                'owner_id': random.choice(customer_ids),
                'global_interest_rate_dec': f.pydecimal(right_digits=2,min_value=1, max_value=30),
                'lombard_rate_dec': f.pydecimal(right_digits=2,min_value=1, max_value=30),
                'product_name': 'L1',
                'amount_requested': random.randint(5000,50000),
                'loan_period': random.randint(6,48),
                'created_date': f.date_between(start_date='-2y'),
            }

            prod = Product.objects.create(**product_params)
            # prod.owner_id = random.choice(customer_ids)
            # prod.save()
            product_ids.append(prod.id)
            obj_count += 1

        for paymt in range(pm):
            pr_id = random.choice(product_ids)
            pr = Product.objects.get(id=pr_id)
            amount = f.pydecimal(right_digits=2,min_value=50, max_value=500)                
            start_date = pr.created_date if not pr.last_payment else pr.last_payment
            payment_date = f.date_between(start_date=start_date)
            pr.last_payment = payment_date
            # payment_params = {
            #     'amount': f.pydecimal(right_digits=2,min_value=50, max_value=500),
            #     'created_date': f.date_between(start_date='-2y'),
            #     'product_id': random.choice(product_ids)
            # }
            Payment.objects.create(
                amount=amount,
                product_id=pr_id,
                created_date=payment_date
                )
            
            pr.tot_paid += amount
            pr.tot_debt = pr.opti_debt(pr.tot_paid, pr.inst_sch)
            pr.tot_delay = pr.opti_delay(pr.tot_paid)
            pr.save()
            obj_count += 1

            
        end = t.time()
        print('\nAdded', obj_count, 'objects in', end-start, 'sec')
