from .models import Customer, Adress
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
    class Meta():

        fields = ['first_name', 'last_name', 'social_security_no_pesel', 'id_passport', 'martial_status', 'phone_no', 'email']
        model = Customer
        widgets = {
            'first_name': TextInput(attrs={'class': 'w3-input w3-border'}),
            'last_name': TextInput(attrs={'class': 'w3-input w3-border'}),
            'social_security_no_pesel' : NumberInput(attrs={'class': 'w3-input w3-border'}),
            'id_passport' : TextInput(attrs={'class': 'w3-input w3-border'}),
            'martial_status': Select(attrs={'class': 'w3-input w3-border'}),
            'phone_no' : NumberInput(attrs={'class': 'w3-input w3-border'}),
            'email' : EmailInput(attrs={'class': 'w3-input w3-border'}),
        }
        labels = {
            'first_name':'First Name',
            'last_name': 'Last Name',
            'social_security_no_pesel': 'PESEL',
            'id_passport' : 'ID no. or Passport no.',
            'martial_status': 'Martial Status',
            'phone_no' : 'Mobile phone number',
            'email' : 'Email adress',

        }
