import re
import datetime
from django.utils.translation import gettext_lazy as _
from rest_framework.serializers import ValidationError
from rest_framework.fields import RegexField


'''
Fields validation below are django-localflavor validators modified to work with DRF

Checksum validation is removed (it would be hard to put in fake data otherwise)
'''


class PhoneNumberFieldDRF(RegexField):

    default_error_messages = {
        'invalid': _('Use the following format: XXX-XXX-XXX or XX-XXX-XX-XX or XXXXXXXXX'),
    }    

    def __init__(self, **kwargs):
        super().__init__(
                r'^\d{3}-\d{3}-\d{3}$|^\d{2}-\d{3}-\d{2}-\d{2}$|^\d{9}$',
                **kwargs
            )

    def run_validation(self, value):
        value = super().run_validation(value)
        value = re.sub("[-]", "", value)
        return '%s' % value


class PLPESELFieldDRF(RegexField):

    default_error_messages = {
        'invalid': _('National Identification Number consists of 11 digits.'),
        'birthdate': _('The National Identification Number contains an invalid birth date.'),
    }

    def __init__(self, **kwargs):
        super().__init__(r'^\d{11}$', **kwargs)

    def run_validation(self, value):
        value = super().run_validation(value)
        if not self.has_valid_birth_date(value):
            raise ValidationError(self.error_messages['birthdate'], code='birthdate')
        return '%s' % value

    def has_valid_birth_date(self, number):
        """
        Checks whether the birth date encoded in PESEL is valid.
        """
        y = int(number[:2])
        m = int(number[2:4])
        d = int(number[4:6])
        md2century = {80: 1800, 0: 1900, 20: 2000, 40: 2100, 60: 2200}
        for md, cent in md2century.items():
            if 1 <= m - md <= 12:
                y += cent
                m -= md
                break
        try:
            self.birth_date = datetime.date(y, m, d)
            return True
        except ValueError:
            return False


class PLNationalIDCardNumberFieldDRF(RegexField):

    default_error_messages = {
        'invalid': _('National ID Card Number consists of 3 letters and 6 digits.'),
    }

    def __init__(self, **kwargs):
        super().__init__(r'^[A-Za-z]{3}\d{6}$', **kwargs)

class PLNIPFieldDRF(RegexField):

    default_error_messages = {
        'invalid': _('Enter a tax number field (NIP) in the format XXX-XXX-XX-XX, XXX-XX-XX-XXX or XXXXXXXXXX.'),
    }

    def __init__(self, **kwargs):
        super().__init__(
            r'^\d{3}-\d{3}-\d{2}-\d{2}$|^\d{3}-\d{2}-\d{2}-\d{3}$|^\d{10}$',
            **kwargs
        )

    def run_validation(self, value):
        value = super().run_validation(value)
        value = re.sub("[-]", "", value)
        return '%s' % value