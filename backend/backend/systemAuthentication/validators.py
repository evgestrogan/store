from django.core import validators
from django.utils.deconstruct import deconstructible


@deconstructible
class UnicodePhoneNumberValidator(validators.RegexValidator):
    regex = r'[0-9]{9}'
    message = 'Введите номер телефона в формате "29ХХХХХХХ", "33ХХХХХХХ", "44ХХХХХХХ"'
    flags = 0
