import datetime, os
from decimal import Decimal
from email.policy import default
import random
from xml.sax.handler import property_declaration_handler
from loan_co_site.storage import OverwriteUploadStorage
from core.validators import validate_file_size
from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ObjectDoesNotExist
from dateutil.relativedelta import relativedelta
from django.urls import reverse
from django.contrib.auth.models import User
from core.helper_methods import ProductMethods

## other


def user_pic_path(instance, filename):
    user_id = instance.user.id
    return f'user_{user_id}/profile_pic/u{user_id}pp.jpeg'
    # not sure if i force .jpeg file extension it will work always... to be tested...

def account_generator():
    return random.randint(10000000, 99999999)

# Create your models here.

class UserInfo(models.Model):
    gender_choices = (
        ('m', 'Male'),
        ('f', 'Female'),
    )    
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    first_name = models.CharField('First Name', max_length=50)
    last_name = models.CharField('Last Name', max_length=50)
    adress = models.ForeignKey('Adress', on_delete=models.SET_NULL, 
                                null=True)
    dob = models.DateField('Date of Birth')
    gender = models.CharField(choices=gender_choices, max_length=2)
    social_security_no_pesel = models.CharField('PESEL', unique=True, 
                                blank=False, null=False, max_length=11)
    id_passport = models.CharField('ID serial number',
                                max_length=9, unique=True, blank=False, 
                                null=False)
    phone_no = models.CharField(unique=True, max_length=9)
    created_date = models.DateField(auto_now_add=True)
    information = models.TextField(null=True, blank=True)
    profile_pic = models.FileField(upload_to=user_pic_path, null=True, blank=True, storage=OverwriteUploadStorage, validators=[validate_file_size])
 

    def __str__(self):
        return self.user.username


class Customer(models.Model):

    martial_choices = (
        ('md', 'Maiden'),
        ('dv', 'Divorced'),
        ('mr', 'Married'),
        ('wd', 'Widow'),
    )

    gender_choices = (
        ('m', 'Male'),
        ('f', 'Female'),
    )

    status_choices = (
        ('ft', 'Full-Time'),
        ('pt', 'Part-Time'),
        ('rt', 'Retired'),
        ('dp', 'Disablement Pension'),
    )

    first_name = models.CharField('First Name', max_length=50)
    last_name = models.CharField('Last Name', max_length=50)
    adress = models.ForeignKey('Adress', on_delete=models.SET_NULL, 
                                null=True)
    dob = models.DateField('Date of Birth')
    gender = models.CharField(choices=gender_choices, max_length=2)
    social_security_no_pesel = models.CharField('PESEL', unique=True, 
                                blank=False, null=False, max_length=11)
    id_passport = models.CharField('ID serial number',
                                max_length=9, unique=True, blank=False, 
                                null=False)
    martial_status = models.CharField(choices=martial_choices, max_length=2)
    work_status = models.CharField(choices=status_choices, max_length=2)
    workplace = models.ForeignKey('Workplace', on_delete=models.SET_NULL, 
                                null=True)
    esd = models.DateField('Employment start date')
    salaty = models.IntegerField(blank=True, null=True)
    position = models.CharField(max_length=50, blank=True, null=True)
    phone_no = models.CharField(unique=True, max_length=9)
    email = models.EmailField(max_length=50, blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, 
                                null=True)
    created_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
    
    def get_absolute_url(self):
        return reverse("create_customer") #kwargs={"pk": self.pk})

    def get_fields(self):
        return [(field.verbose_name, field.value_from_object(self)) for field in self.__class__._meta.fields]



class Adress(models.Model):
    street = models.CharField(max_length=50)
    zip_code = models.CharField(max_length=6)
    city = models.CharField(max_length=50)
    building_no = models.CharField(max_length=5)

    def __str__(self):
        return f'{self.zip_code}, {self.city}, {self.street} {self.building_no}'

class Workplace(models.Model):

    id_nip = models.CharField(unique=True, max_length=10)
    name = models.CharField(max_length=50)
    adress = models.ForeignKey('Adress', on_delete=models.SET_NULL, null=True)
    phone_no = models.CharField(unique=True, max_length=9)
    email = models.EmailField(max_length=50, blank=True, null=True)

    def __str__(self):
        return f'{self.name}'

class Product(models.Model, ProductMethods):

    products = (
        ('L1', 'Loan'),
        ('L2', 'Loan - good Credit Rating'),
    )  
      
    owner = models.ForeignKey('Customer', on_delete=models.CASCADE,
                                    null=True, blank=True)
                               
    global_interest_rate_dec = models.DecimalField('Central banks\n interest rate in %',
                                    validators=[MinValueValidator(0),
                                    MaxValueValidator(30)], blank=False, default=Decimal('5.25'),
                                    max_digits=4, decimal_places=2)
    lombard_rate_dec = models.DecimalField('Central banks lombard\n interest rate in %',
                                    validators=[MinValueValidator(0),
                                    MaxValueValidator(30)], blank=False, default=Decimal('5.75'),
                                    max_digits=4, decimal_places=2)
    product_name = models.CharField(choices = products, max_length=2,
                                    default='L1')
    amount_requested = models.IntegerField(validators=[MinValueValidator(2000), 
                                    MaxValueValidator(50000)], 
                                    default=10000, blank=False)
    loan_period = models.IntegerField(choices=list(zip(range(6, 49), range(6, 49))),
                                    blank=False, default=24)
    created_date = models.DateField(auto_now_add=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.payments_query = Payment.objects.filter(product=self.id)
        self.complete = []

    def __str__(self):
        return f'ID: {self.id}, Owner {self.owner.id}, amount: {self.amount_requested}, period: {self.loan_period}'


class Payment(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    created_date = models.DateField(auto_now_add=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return f'Product: {self.product.id}, amount: {self.amount}, date: {self.created_date} '

