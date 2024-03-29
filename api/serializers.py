
from rest_framework import serializers

from api.validators import (PhoneNumberFieldDRF,
                            PLNationalIDCardNumberFieldDRF, PLNIPFieldDRF,
                            PLPESELFieldDRF)
from core.models import Adress, Customer, Product, UserInfo, Workplace


class AdressSerializer(serializers.ModelSerializer):

    class Meta:
        model = Adress
        exclude = [
            'id',
        ]


class WorkplaceSerializer(serializers.ModelSerializer):

    adress = AdressSerializer()
    phone_no = PhoneNumberFieldDRF()

    id_nip = PLNIPFieldDRF()

    class Meta:
        model = Workplace
        exclude = [
            'id',
        ]
        # Unique Validators are removed because DRF doesnt know how to deal
        # with unique validation on nested serializers when updating data
        extra_kwargs = {
            'id_nip': {'validators': []},
            'phone_no': {'validators': []}
        }


class DynamicFieldsModelSerializer(serializers.ModelSerializer):

    # Copy/paste official DRF docs
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


class CustomerDetailsSerializer(serializers.ModelSerializer):
    adress = AdressSerializer()
    workplace = WorkplaceSerializer()
    url = serializers.HyperlinkedIdentityField(
        view_name='customer_detail',
        read_only=True,
        lookup_field='pk'
    )

    class Meta:
        model = Customer
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    owner = CustomerDetailsSerializer()

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


class UserInfoSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserInfo
        fields = [
            'first_name',
            'last_name',
            'phone_no',
            'user',
            'created_date'
        ]


class PDFProductSeriaziler(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    owner = CustomerDetailsSerializer()

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
            'created_date',
            'create_schedule',
            'user'
            ]

    def get_user(self, *args, **kwargs):
        request = self.context.get('request')
        user_id = request.user.id
        user_inst = UserInfo.objects.get(user=user_id)
        user = UserInfoSerializer(user_inst)
        return user.data
