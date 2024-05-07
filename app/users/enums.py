from django.db import models
from enum import unique


@unique
class UserType(models.IntegerChoices):
    MEMBER = 1, 'Member'
    PRESIDENT = 2, 'President'
