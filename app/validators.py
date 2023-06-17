from rest_framework.exceptions import ValidationError


def custom_title_validator(value):
    if len(value) < 5:
        raise ValidationError("Title must be at least 5 characters long.")
