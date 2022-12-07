import re
from django.core.exceptions import ValidationError
from django.forms.fields import RegexField
from django.utils.translation import gettext_lazy as _
from localflavor.pl.forms import (PLPESELField,
                    PLNationalIDCardNumberField,
                    PLNIPField)

def validate_file_size(value):
    filesize = value.size

    if filesize > 1048576:
        raise ValidationError("File must be smaller than 1.0 MB")
    else:
        return value



class PESELwithoutChecksum(PLPESELField):
    def has_valid_checksum(self, number):
        return True

class IDwithoutChecksum(PLNationalIDCardNumberField):
    def has_valid_checksum(self, number):
        return True

class NIPwithoutChecksum(PLNIPField):
    def has_valid_checksum(self, number):
        return True

class PhoneNumberField(RegexField):

    default_error_messages = {
        'invalid': _('Use the following format: XXX-XXX-XXX or XX-XXX-XX-XX or XXXXXXXXX'),
    }    

    def __init__(self, **kwargs):
        super().__init__(
                r'^\d{3}-\d{3}-\d{3}$|^\d{2}-\d{3}-\d{2}-\d{2}$|^\d{9}$',
                **kwargs
            )

    def clean(self, value):
        value = super().clean(value)
        if value in self.empty_values:
            return self.empty_value
        value = re.sub("[-]", "", value)
        return '%s' % value