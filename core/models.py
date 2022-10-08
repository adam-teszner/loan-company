import datetime
from email.policy import default
import random
from xml.sax.handler import property_declaration_handler
from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.core.validators import MinValueValidator, MaxValueValidator
from dateutil.relativedelta import relativedelta
from django.urls import reverse
from django.contrib.auth.models import User

## other

def user_pic_path(instance, filename):
    return 'user_{0}/profile_pic/{1}'.format(instance.user.id, filename)

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
    social_security_no_pesel = models.IntegerField('PESEL', unique=True, 
                                blank=False, null=False)
    id_passport = models.CharField('ID serial number or Passport serial number',
                                max_length=10, unique=True, blank=False, 
                                null=False)
    phone_no = models.IntegerField(unique=True)
    created_date = models.DateField(auto_now_add=True)
    information = models.TextField(null=True, blank=True)
    profile_pic = models.FileField(upload_to=user_pic_path, null=True, blank=True)
    

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
    social_security_no_pesel = models.IntegerField('PESEL', unique=True, 
                                blank=False, null=False)
    id_passport = models.CharField('ID serial number or Passport serial number',
                                max_length=10, unique=True, blank=False, 
                                null=False)
    martial_status = models.CharField(choices=martial_choices, max_length=2)
    work_status = models.CharField(choices=status_choices, max_length=2)
    workplace = models.ForeignKey('Workplace', on_delete=models.SET_NULL, 
                                null=True)
    esd = models.DateField('Employment start date')
    salaty = models.IntegerField(blank=True, null=True)
    position = models.CharField(max_length=50, blank=True, null=True)
    phone_no = models.IntegerField(unique=True)
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

    id_nip = models.IntegerField(unique=True)
    name = models.CharField(max_length=50)
    adress = models.ForeignKey('Adress', on_delete=models.SET_NULL, null=True)
    phone_no = models.IntegerField(unique=True)
    email = models.EmailField(max_length=50, blank=True, null=True)

    def __str__(self):
        return f'{self.name}'

class Product(models.Model):

    products = (
        ('L1', 'Loan'),
        ('L2', 'Loan - good Credit Rating'),
    )  
      
    owner = models.ForeignKey('Customer', on_delete=models.CASCADE,
                                    null=True, blank=True)
    global_interest_rate = models.FloatField('Central banks\n interest rate in %', 
                                    validators=[MinValueValidator(0), 
                                    MaxValueValidator(30)], blank=False,
                                    default=5.25)
    lombard_rate = models.FloatField('Central banks lombard\n interest rate in %',
                                    validators=[MinValueValidator(0), 
                                    MaxValueValidator(30)], blank=False,
                                    default=5.75)
    product_name = models.CharField(choices = products, max_length=2,
                                    default='L1')
    amount_requested = models.IntegerField(validators=[MinValueValidator(2000), 
                                    MaxValueValidator(50000)], 
                                    default=10000, blank=False)
    loan_period = models.IntegerField(choices=list(zip(range(6, 49), range(6, 49))),
                                    blank=False, default=24)
    created_date = models.DateField(auto_now_add=True)
    
    
    @property
    def days_since_create(self):
        today = datetime.date.today()
        try:
            days_passed = today - self.created_date
            days_passed_split = str(days_passed).split(' ')
            return int(days_passed_split[0])
        except:
            return 0
 
    @property
    def total_amount(self):
        return round(self.installments*self.loan_period,2)


    @property
    def installments(self):
              
        p = (self.global_interest_rate/100*2)/12
        nu = p*((1+p)**self.loan_period)
        de = ((1+p)**self.loan_period)-1
        total = self.amount_requested * (nu/de)
        if self.product_name == 'L1':
            return round(total + (0.15*total), 2)
        else:
            return round(total, 2)

    def __str__(self):
        return f'ID: {self.id}, amount: {self.amount_requested}, period: {self.loan_period}'

    @property
    def installement_schedule(self):
        try:
            z = []
            for x in range(1, self.loan_period+1):
                
                z.append(f'{x} - amount: -- {self.installments} ---- Required by: -- {self.created_date + relativedelta(months=x)}')
            return '\n'.join(z)
            # return z
        except:
            return 'You must create a loan first ! '


    @property
    def installment_dict(self):
        try:
            installments = {}
            for x in range(1, self.loan_period+1):
                installments[x] = {
                    'amount' : self.installments,
                    'required by' : str(self.created_date + relativedelta(months=x))
                }
                # installments['amount'] = self.installments
                # installments['required by'] = self.created_date + relativedelta(months=x)
            return installments
        except:
            return 'NO Loans'

    def inst_sch(self):
        schedule = []
        for x in range(1, self.loan_period+1):
            schedule.append((x, self.installments, self.created_date + relativedelta(months=x)))
        return schedule

    @property
    def get_payments(self):
        payments = Payment.objects.filter(product=self.id)
        payment_list = []
        for payment in payments:
            payment_list.append((payment.created_date, payment.amount))
        return sorted(payment_list)


    @property
    def paid_total(self):
        paid_total = 0
        for (a,b) in self.get_payments:
            paid_total = paid_total + b
        return paid_total


    @property
    def paid_by_day(self):
        daily_payements = {}
        for a,b in self.get_payments:
            if a in daily_payements:
                daily_payements[a] += b
            else:
                daily_payements[a] = b
        return daily_payements

    def paid_by_day_human(self):
        x = [f'{a} -- {b}' for (a,b) in self.paid_by_day.items()]
        return '\n'.join(x)

    def payments_human(self):
        x = [f'{a} -- {b}' for (a,b) in self.get_payments]
        return '\n'.join(x)
        


class Payment(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    created_date = models.DateField(auto_now_add=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2)

'''

    #### extending product 

    account_no = models.IntegerField(default=account_generator)


    # create balance field (how much is paid total) 
    # paid_installments = []
    paid_installments = ArrayField(
        models.CharField(max_length=30), default=list, null=True, blank=True
    )

    # create ability to "pay" (like an ATM)

    def pay_installment(self, amount):
        date = str(datetime.date.today())
        self.paid_installments.append((date, amount))

    # sum all payments by day
    @property
    def payment_day_by_day(self):
        daily_payements = {}
        for k,v in self.paid_installments:
            if k in daily_payements:
                daily_payements[k] += v
            else:
                daily_payements[k] = v
        return daily_payements
    @property
    def paid_total(self):
        paid_total = 0
        for k,v in self.paid_installments:
            paid_total = paid_total + v
        return paid_total

    # connect payments to installements (product installements schedule)
    # by tuples ? (ammount, date) ??

    # create debt field(from schedule)

    ### other, scoring, interest ?? ###    

            

####  Maybe use django-moeny ???

class ProductBankAccount(models.Model):

    product = models.OneToOneField(Product, on_delete=models.CASCADE)
    account_no = models.IntegerField(default=account_generator)


    # create balance field (how much is paid total) 
    # paid_installments = []
    paid_installments = ArrayField(
        models.CharField(max_length=30), default=list
    )

    # create ability to "pay" (like an ATM)

    def pay_installment(self, amount):
        date = str(datetime.date.today())
        self.paid_installments.append((date, amount))

    # sum all payments by day

    def payment_day_by_day(self):
        daily_payements = {}
        for k,v in self.paid_installments:
            if k in daily_payements:
                daily_payements[k] += v
            else:
                daily_payements[k] = v
        return daily_payements

    def paid_total(self):
        paid_total = 0
        for k,v in self.paid_installments:
            paid_total + v
        return paid_total

    # connect payments to installements (product installements schedule)
    # by tuples ? (ammount, date) ??

    # create debt field(from schedule)

    ### other, scoring, interest ?? ###    



'''

