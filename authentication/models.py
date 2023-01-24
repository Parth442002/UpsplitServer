from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.core.validators import RegexValidator
from .manager import NewUserAccountManager
import uuid


class Account(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    #email = models.EmailField(unique=True)
    username = models.CharField(max_length=150, unique=True)
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$', message="Please enter a valid phone number")
    phone_number = models.CharField(
        validators=[phone_regex], max_length=17, unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)

    objects = NewUserAccountManager()
    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['username', ]

    def __str__(self):
        return self.username
