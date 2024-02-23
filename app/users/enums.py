from django.db import models
from enum import unique


@unique
class Role(models.IntegerChoices):
    ADMIN = 1, 'Admin'
    EMPLOYEE = 2, 'Employee'
    CUSTOMER = 3, 'Customer'
