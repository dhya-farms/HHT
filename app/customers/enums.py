from django.db import models


class AddressType(models.IntegerChoices):
    HOME = 1, 'Home'
    WORK = 2, 'Work'
    OTHER = 3, 'Other'

