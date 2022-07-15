from tokenize import Number
from .models import Customer, Adress, UserInfo, Workplace, Product
from django import forms
from django.forms.widgets import *




class CustCreateAdressForm(forms.ModelForm):
    class Meta():

        fields = '__all__'
        model = Adress
        widgets = {
            'street': TextInput(attrs={'class': 'w3-input w3-border'}),
            'city' : TextInput(attrs={'class': 'w3-input w3-border'}),
            'building_no': TextInput(attrs={'class': 'w3-input w3-border'}),
            'zip_code': NumberInput(attrs={'class': 'w3-input w3-border'}),
        }

        labels = {
            'street' : 'Street',
            'city': 'City',
            'building_no' : 'Building no/flat no',
            'zip_code' : 'Zip Code',
        }

class CustCreatePersonalInfo(forms.ModelForm):
    # dob = forms.DateField(input_formats=['%Y-%m-%d'])
    # esd = forms.DateField(input_formats=['%Y-%m-%d'])


    class Meta():

        fields = ['first_name', 'last_name', 'dob', 'gender', 'social_security_no_pesel',
                'id_passport', 'martial_status', 'phone_no', 'email', 'esd', 'work_status', 'salaty', 'position']
        model = Customer
        widgets = {
            'first_name': TextInput(attrs={'class': 'w3-input w3-border'}),
            'last_name': TextInput(attrs={'class': 'w3-input w3-border'}),
            'dob': DateInput(format='%Y-%m-%d', attrs={'class': 'w3-input w3-border', 
                                    'type': 'date'}),
            'gender': Select(attrs={'class': 'w3-input w3-border'}),
            'social_security_no_pesel' : NumberInput(attrs={'class': 'w3-input w3-border'}),
            'id_passport' : TextInput(attrs={'class': 'w3-input w3-border'}),
            'martial_status': Select(attrs={'class': 'w3-input w3-border'}),
            'work_status' : Select(attrs={'class': 'w3-input w3-border'}),
            'esd': DateInput(format='%Y-%m-%d', attrs={'class': 'w3-input w3-border', 
                                    'type': 'date'}),
            'phone_no' : NumberInput(attrs={'class': 'w3-input w3-border'}),
            'email' : EmailInput(attrs={'class': 'w3-input w3-border'}),
            'salaty' : NumberInput(attrs={'class': 'w3-input w3-border'}),
            'position': TextInput(attrs={'class': 'w3-input w3-border'}),
            # 'created_by': Select(attrs={'class': 'w3-input w3-border'})
        }
        labels = {
            'first_name':'First Name',
            'last_name': 'Last Name',
            'dog' : 'Date of Birth',
            'gender' : 'Sex',
            'social_security_no_pesel': 'PESEL',
            'id_passport' : 'ID no. or Passport no.',
            'martial_status': 'Martial Status',
            'phone_no' : 'Mobile phone number',
            'email' : 'Email adress',
            'work_status' : 'Income source',
            'esd' : 'Employment start date',
            'salaty': 'Net Income',
            'position' : 'Job Position',
            # 'created_by' : 'Created By',

        }

class CustomWorkplaceForm(forms.ModelForm):

    class Meta():
        model = Workplace
        exclude = ('adress',) 

        widgets = {
            'name' : TextInput(attrs={'class': 'w3-input w3-border'}),
            'id_nip': NumberInput(attrs={'class': 'w3-input w3-border'}),
            'phone_no':  NumberInput(attrs={'class': 'w3-input w3-border'}),
            'email': EmailInput(attrs={'class': 'w3-input w3-border'}),
        }

        labels = {
            'id_nip': 'NIP',
            'name': 'Company Name',
        }
        

class AddNewProductForm(forms.ModelForm):

    class Meta():
        model = Product
        exclude = ('created_date', 'owner',)


class CustomSignUpForm(forms.ModelForm):
    class Meta():
        model = UserInfo
        fields = ['first_name', 'last_name', 'dob', 'gender',
                'social_security_no_pesel', 'id_passport', 'phone_no',
                'information']