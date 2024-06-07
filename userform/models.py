from django.db import models
from django.core.exceptions import ValidationError

def validate_phone(value):
    if len(value) != 10 or not value.isdigit():
        raise ValidationError('Phone number must be exactly 10 digits.')

class User(models.Model):
    full_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    email = models.EmailField()
    phone = models.CharField(max_length=10, validators=[validate_phone])
    nationality = models.CharField(max_length=50)

    def __str__(self):
        return self.full_name
