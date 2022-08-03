from .models import Customer, Adress, UserInfo, Workplace, Product
from django import forms
from django.forms.widgets import *




class CustCreateAdressForm(forms.ModelForm):
    class Meta():

        fields = '__all__'
        model = Adress
        widgets = {
            'street': TextInput(attrs={'class': 'pyl-input'}),
            'city' : TextInput(attrs={'class': 'pyl-input'}),
            'building_no': TextInput(attrs={'class': 'pyl-input'}),
            'zip_code': NumberInput(attrs={'class': 'pyl-input'}),
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
            'first_name': TextInput(attrs={'class': 'pyl-input'}),
            'last_name': TextInput(attrs={'class': 'pyl-input'}),
            'dob': DateInput(format='%Y-%m-%d', attrs={'class': 'pyl-input', 
                                    'type': 'date'}),
            'gender': Select(attrs={'class': 'pyl-input'}),
            'social_security_no_pesel' : NumberInput(attrs={'class': 'pyl-input', 'onfocusout': 'checkPesel()'}),
            'id_passport' : TextInput(attrs={'class': 'pyl-input'}),
            'martial_status': Select(attrs={'class': 'pyl-input'}),
            'work_status' : Select(attrs={'class': 'pyl-input'}),
            'esd': DateInput(format='%Y-%m-%d', attrs={'class': 'pyl-input', 
                                    'type': 'date'}),
            'phone_no' : NumberInput(attrs={'class': 'pyl-input'}),
            'email' : EmailInput(attrs={'class': 'pyl-input'}),
            'salaty' : NumberInput(attrs={'class': 'pyl-input'}),
            'position': TextInput(attrs={'class': 'pyl-input'}),
            # 'created_by': Select(attrs={'class': 'pyl-input'})
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

class CustCreatePersonalInfoUpdate(CustCreatePersonalInfo):
    class Meta(CustCreatePersonalInfo.Meta):
        exclude = ('first_name', 'gender', 'dob', 'social_security_no_pesel')

class CustomWorkplaceForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(CustomWorkplaceForm, self).__init__(*args, **kwargs)
        self.auto_id = 'workplace_id_%s'

    class Meta():
        model = Workplace
        exclude = ('adress',) 
        widgets = {
            'name' : TextInput(attrs={'class': 'pyl-input'}),
            'id_nip': NumberInput(attrs={'class': 'pyl-input'}),
            'phone_no':  NumberInput(attrs={'class': 'pyl-input'}),
            'email': EmailInput(attrs={'class': 'pyl-input'}),
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