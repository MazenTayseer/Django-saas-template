import uuid

import uuid_utils
from django.db import models


def _uuid7_default():
    """Return a standard uuid.UUID (Django-compatible) from uuid7."""
    return uuid.UUID(hex=uuid_utils.uuid7().hex)


class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=_uuid7_default, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
