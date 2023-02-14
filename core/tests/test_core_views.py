import datetime
import json
from faker import Faker
from django.test import TestCase, RequestFactory, Client
from django.core import serializers
from core.views import *
from core.urls import *
from core.models import (Customer, Adress, Workplace,
                UserInfo)
from core.forms import (CustCreatePersonalInfo,
                CustCreateAdressForm, CustomWorkplaceForm)
from django.contrib.auth.models import User, AnonymousUser
from django.http import QueryDict


class TestCreateCustomerView(TestCase):
    def setUp(self) -> None:
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username='tester', email='tete@tete.pl', password='testete1123', id=1
        )
        self.create_url = reverse('custom_create')
        self.client = Client()
        f = Faker()
        f_pl = Faker('pl_PL')

        def fake_number_digits(faker_inst:object, digits:int) -> str:
            '''
            generates unique number with defined number of digits,
            even when first digits are zeros
            '''
            number: str = str(faker_inst.unique.random_number(digits=digits))
            if len(number) < 9:
                prec_zeros: int = 9 - len(number)
                return prec_zeros*'0'+number
            return number


        self.adress = Adress.objects.create(
            street='taka',
            city='grad',
            zip_code='44-240',
            building_no='13'
        )

        self.workplace = Workplace.objects.create(
            name='tamtomiejsce',
            id_nip='1234567890',
            adress=self.adress,
            phone_no='777333222',

        )
        self.user_info = UserInfo.objects.create(
            first_name='Adam',
            last_name='TESZNER',
            id=1,
            dob=datetime.date(2022,3,1),
            user=self.user
        )
        self.customer = Customer.objects.create(
            first_name='Ada',
            last_name='TETE',
            dob=datetime.date(2000,10,1),
            gender='m',
            social_security_no_pesel='92043002800',
            id_passport="ADA123456",
            martial_status='dv',
            work_status='rt',
            esd=datetime.date(2002,11,1),
            phone_no=fake_number_digits(f,9),
            created_by=self.user,
            created_date=datetime.date(2003,12,1),
            adress=self.adress,
            workplace=self.workplace,
        )

        self.customer.adress.save()
        self.customer.workplace.adress.save()
        
        self.adress_params = {
            'building_no': f.building_number(),
            'city': f.city(),
            'street': f.street_name(),
            'zip_code': f_pl.zipcode(),
            }
        self.work_adress_params = {
            'building_no': f.building_number(),
            'city': f.city(),
            'street': f.street_name(),
            'zip_code': f_pl.zipcode(),
            }
        self.workplace_params = {
            'email': f.ascii_email(),
            'id_nip': f_pl.unique.nip(),
            'name': f.company(),
            'phone_no': fake_number_digits(f,9),
            'adress': self.work_adress_params,
            }
        self.customer_params = {
            # 'created_by_id': self.user_info.id,
            'created_date': datetime.date.today(),
            'dob': f.date_of_birth(minimum_age=18, maximum_age=70),
            'email': f.ascii_email(),
            'esd': f.date_between(start_date='-48y', end_date='-18y'),
            'first_name': f.first_name(),
            'gender': 'm',
            'id_passport': f_pl.unique.identity_card_number(),
            'last_name': f.last_name(),
            'martial_status': 'mr',
            'phone_no': fake_number_digits(f,9),
            'position': f.job()[:40]+'...',
            'salaty': f.random_number(digits=4),
            'social_security_no_pesel': f_pl.unique.pesel(),
            'work_status': 'ft',
            'adress': self.adress_params,
            'workplace': self.workplace_params
            }
        



        self.fake_customer = {
            'customer': {
                # 'created_by_id': self.user_info.id,
                # 'created_date': datetime.date.today(),
                # 'id': f.unique.random_number(digits=3),
                'dob': f.date_of_birth(minimum_age=18, maximum_age=70),
                'email': f.ascii_email(),
                'esd': f.date_between(start_date='-48y', end_date='-18y'),
                'first_name': f.first_name(),
                'gender': 'm',
                'id_passport': f_pl.unique.identity_card_number(),
                'last_name': f.last_name(),
                'martial_status': 'mr',
                'phone_no': fake_number_digits(f,9),
                # 'phone_no': '111222333',
                'position': f.job()[:40]+'...',
                'salaty': f.random_number(digits=4),
                'social_security_no_pesel': f_pl.unique.pesel(),
                'work_status': 'ft',
                # 'adress': self.adress_params,
                # 'workplace': self.workplace_params
                },
            'adress' : {
                'building_no': f.building_number(),
                'city': f.city(),
                'street': f.street_name(),
                'zip_code': f_pl.zipcode(),
                },
            'workplace' : {
                'email': f.ascii_email(),
                'id_nip': f_pl.unique.nip(),
                'name': f.company(),
                'phone_no': fake_number_digits(f,9),
                # 'phone_no': '999888222',
                # 'adress': self.work_adress_params,
                },
            'work_adr' : {
                'building_no': f.building_number(),
                'city': f.city(),
                'street': f.street_name(),
                'zip_code': f_pl.zipcode(),
                },
        }

        return super().setUp()
    
    def test_create_customer(self) -> None:
        request = self.factory.get(self.create_url)

        # request.user = AnonymousUser()
        request.user = self.user

        response = custom_customer(request)
        self.assertEqual(response.status_code, 200)

    def test_create_customer_get_pesel(self) -> None:
        self.client.force_login(self.user)
        response = self.client.get(self.create_url, data={
            'pesel': '92043002800'
        })

        customer_data = serializers.serialize('json', [self.customer])
        customer_adr = serializers.serialize('json', [self.customer.adress])
        workplace_data = serializers.serialize('json', [self.customer.workplace])
        workplace_adress_data = serializers.serialize('json', [self.customer.workplace.adress])
        customer_creator = UserInfo.objects.get(user=self.customer.created_by.id)

        json_list = [customer_data, customer_adr, workplace_data, workplace_adress_data]
        data_2 = []
        for item in json_list:
            data_2.extend(json.loads(item))

        data_2.append({
            'creator_first_name' : customer_creator.first_name,
            'creator_last_name' : customer_creator.last_name
            })

        merged_json = json.dumps(data_2, indent=2)

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(str(response.content, encoding='utf8'), merged_json)


    def test_create_customer_post_customer_id_none(self) -> None:
        self.client.login(username='tester', password='testete1123')
        #### to był problem !!!! nie moze byc abstract user !! czyli force_login ! wiadomo, wtedy za chiny nie zwaliduje tego...
        
        cust_data = self.fake_customer['customer']
        cust_adr = self.fake_customer['adress']
        cust_workplc = self.fake_customer['workplace']
        workplc_adr = self.fake_customer['work_adr']

        for k,v in cust_adr.copy().items():
            new = 'customer_adress-' + k
            cust_adr[new] = v
            cust_adr.pop(k)

        for k,v in cust_workplc.copy().items():
            new = 'workplace_form-' + k
            cust_workplc[new] = v
            cust_workplc.pop(k)

        for k,v in workplc_adr.copy().items():
            new = 'workplace_adr_form-' + k
            workplc_adr[new] = v
            workplc_adr.pop(k)            
            
        qd = QueryDict('', mutable=True)


        data = {
            **cust_data,
            **cust_adr,
            **cust_workplc,
            **workplc_adr
        }
        data['customer_id_value'] = ''
        qd.update(data)
        
        response = self.client.post(self.create_url, data=data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('customer_detail', args=[2]))


    def test_create_customer_post_customer_id(self) -> None:
        self.client.login(username='tester', password='testete1123')
        pass        