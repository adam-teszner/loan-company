from .models import Customer, Adress, Product
from django import forms


class CustCreatePersonalInfo(forms.ModelForm):
    class Meta():

        fields = '__all__'
        model = Customer

class CustCreateAdressForm(forms.ModelForm):
    class Meta():

        fields = '__all__'
        model = Adress




