
from rest_framework import serializers
from api.validators import (PhoneNumberFieldDRF,
                            PLPESELFieldDRF, PLNationalIDCardNumberFieldDRF,
                            PLNIPFieldDRF)

from core.models import (Customer, Adress, Workplace,
                        Product)


class AdressSerializer(serializers.ModelSerializer):

    class Meta:
        model = Adress
        # fields = '__all__'
        exclude = [
            'id',
        ]


class WorkplaceSerializer(serializers.ModelSerializer):

    adress = AdressSerializer()
    phone_no = PhoneNumberFieldDRF()

    id_nip = PLNIPFieldDRF()

    class Meta:
        model = Workplace
        # fields = '__all__'
        exclude = [
            'id',
        ]
        # Unique Validators are removed because DRF doesnt know how to deal with unique
        # validation on nested serializers when updating data
        extra_kwargs = {
            'id_nip': {'validators' : []},
            'phone_no': {'validators': []}
        }

class DynamicFieldsModelSerializer(serializers.ModelSerializer):

    #copy/paste official DRF docs
    """
    A ModelSerializer that takes an additional `fields` argument that
    controls which fields should be displayed.
    """


    def __init__(self, *args, **kwargs):
        # Don't pass the 'fields' arg up to the superclass
        fields = kwargs.pop('fields', None)

        # Instantiate the superclass normally
        super().__init__(*args, **kwargs)

        if fields is not None:
            # Drop any fields that are not specified in the `fields` argument.
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)



class CustomerSerializer(DynamicFieldsModelSerializer):

    adress = AdressSerializer()
    workplace = WorkplaceSerializer()

    phone_no = PhoneNumberFieldDRF()
    social_security_no_pesel = PLPESELFieldDRF()
    id_passport = PLNationalIDCardNumberFieldDRF()

    class Meta:
        model = Customer
        fields = '__all__'
 

    def update(self, cust_inst, validated_data):

        for k, v in validated_data.items():
            if k == 'adress':
                adr_inst = cust_inst.adress
                for akey, aval in validated_data['adress'].items():
                    setattr(adr_inst, akey, aval)

            elif k == 'workplace':
                workplace_inst = cust_inst.workplace
                for wkey, wval in validated_data['workplace'].items():
                    if wkey == 'adress':
                        workplace_adr_inst = cust_inst.workplace.adress
                        for wakey, waval in validated_data['workplace']['adress'].items():
                            setattr(workplace_adr_inst, wakey, waval)
                    else:
                        setattr(workplace_inst, wkey, wval)
            else:
                setattr(cust_inst, k, v)

        cust_inst.save()
        cust_inst.adress.save()
        cust_inst.workplace.save()
        cust_inst.workplace.adress.save()

        return cust_inst


class ProductSerializer(serializers.ModelSerializer):
    owner = CustomerSerializer()

    class Meta:
        model = Product
        fields = [
            'owner',
            'id',
            'amount_requested',
            'loan_period',
            'tot_paid',
            'tot_amout',
            'tot_debt',
            'tot_delay',
            'created_date'
            ]



