from django.core.exceptions import ValidationError

def validate_file_size(value):
    filesize = value.size

    if filesize > 524288:
        raise ValidationError("Max file size is 0.5 MB")
    else:
        return value