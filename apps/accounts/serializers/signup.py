from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework import serializers

User = get_user_model()


class SignupSerializer(serializers.Serializer):
    email = serializers.EmailField(required=False)
    phone_number = PhoneNumberField(required=False)
    password = serializers.CharField(write_only=True)
    first_name = serializers.CharField(required=False, max_length=255)
    last_name = serializers.CharField(required=False, max_length=255)

    def validate(self, attrs):
        email = attrs.get("email")
        phone_number = attrs.get("phone_number")

        if not email and not phone_number:
            raise serializers.ValidationError("At least one of email or phone number is required.")

        errors = {}
        if email and User.objects.filter(email__iexact=email).exists():
            errors["email"] = "A user with this email already exists."
        if phone_number and User.objects.filter(phone_number=phone_number).exists():
            errors["phone_number"] = "A user with this phone number already exists."
        if errors:
            raise serializers.ValidationError(errors)

        user = User(
            email=email,
            phone_number=phone_number,
            first_name=attrs.get("first_name", None),
            last_name=attrs.get("last_name", None),
        )
        try:
            validate_password(attrs["password"], user=user)
        except ValidationError as e:
            raise serializers.ValidationError({"password": e.messages})

        return attrs

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)
        try:
            user.full_clean()
            user.save()
        except (IntegrityError, ValidationError):
            raise serializers.ValidationError("A user with this email or phone number already exists.")
        return user
