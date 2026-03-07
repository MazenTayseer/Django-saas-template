from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q

User = get_user_model()


class EmailOrPhoneBackend(ModelBackend):
    """Authenticates against email or phone_number with password."""

    def authenticate(self, request, identifier=None, password=None, **kwargs):
        if not identifier or not password:
            return None

        try:
            user = User.objects.get(Q(email__iexact=identifier) | Q(phone_number=identifier))
        except (User.DoesNotExist, User.MultipleObjectsReturned):
            # Run the default password hasher to mitigate timing attacks
            User().set_password(password)
            return None

        if user.check_password(password) and self.user_can_authenticate(user):
            return user
        return None
