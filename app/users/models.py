from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.validators import RegexValidator
from django.db.models import JSONField
from django.urls import reverse
from django.db import models
from app.users.enums import UserType
from django.utils.translation import gettext_lazy as _

from app.utils.helpers import generate_random_username
import uuid

class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username_validator = UnicodeUsernameValidator()

    name = models.CharField(max_length=255)
    # username = models.CharField(
    #     _('username'),
    #     max_length=150,
    #     help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
    #     validators=[username_validator],
    #     error_messages={
    #         'unique': _("A user with that username already exists."),
    #     },
    #     default=generate_random_username()
    # )
    email = models.EmailField(_('email address'), unique=True)
    mobile_no = models.CharField(max_length=10, unique=True, validators=[
        RegexValidator(regex=r'^\d{10}$', message="Provide Proper 10 digit Phone Number")],
                                 db_index=True, blank=True, null=True)
    user_type = models.IntegerField(choices=UserType.choices, default=UserType.MEMBER, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    favorites = models.ManyToManyField('products.Product', related_name='favorited_by', blank=True)

    def __str__(self):
        return f"id: {self.id}. {self.name} [{self.mobile_no}]"

    def get_absolute_url(self):
        """Get url for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("users:detail", kwargs={"mobile_no": self.mobile_no})

