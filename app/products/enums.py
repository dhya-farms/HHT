from django.db import models


class DiscountType(models.IntegerChoices):
    PERCENTAGE = 1, 'Percentage'
    FIXED_AMOUNT = 2, 'Fixed Amount'
