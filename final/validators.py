from django.core.exceptions import ValidationError


def validate_user(param):
    if len(param) < 3:
        raise ValidationError('User name is too short')
    if len(param) > 20:
        raise ValidationError('User name is too long')


def validate_password(param):
    if len(param) < 5:
        raise ValidationError('Password name is too short, should have at least 5 characters')
    if len(param) > 21:
        raise ValidationError('Password name is too long, max is 20 characters')
