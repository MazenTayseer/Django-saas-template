from django.contrib.auth.models import AbstractUser, Group
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from apps.core.models.base import BaseModel


class User(AbstractUser, BaseModel):
    # Removing AbstractUser fields
    username = None

    # Basic fields
    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(unique=True, null=True, blank=True)
    phone_number = PhoneNumberField(unique=True, null=True, blank=True)

    # Social fields
    google_id = models.CharField(max_length=255, null=True, blank=True)

    groups = models.ManyToManyField(
        Group, related_name="users", blank=True, help_text="The groups this user belongs to."
    )
    user_permissions = models.ManyToManyField(
        "auth.Permission", related_name="users", blank=True, help_text="Specific permissions for this user."
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        app_label = "core"
        db_table = "users"
