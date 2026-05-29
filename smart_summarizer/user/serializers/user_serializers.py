from rest_framework import serializers
from user.models import User


class UserSerializer(serializers.ModelSerializer):
    """For registration and profile updates."""

    password = serializers.CharField(
        write_only=True,
        max_length=128,
        style={"input_type": "password"},
    )

    class Meta:
        model = User
        fields = '__all__'
        read_only_fields = ["id", "user_id", "creation_date", "updation_date"]

    def validate_user_name(self, value):
        qs = User.objects.filter(user_name=value)
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise serializers.ValidationError("Username already exists.")
        return value

    def validate_email_id(self, value):
        if "@" not in value:
            raise serializers.ValidationError("enter a valid email address.")
        qs = User.objects.filter(email_id=value)
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise serializers.ValidationError("email already exists.")
        return value

    def validate_password(self, value):
        if len(value) < 6:
            raise serializers.ValidationError("Password must be at least 6 characters.")
        return value


class UserResponseSerializer(serializers.ModelSerializer):
    """returning user data in responses. Never exposes the password."""

    class Meta:
        model = User
        exclude = ['password']


class LoginSerializer(serializers.Serializer):
    """Validates login input: email + password."""

    email = serializers.EmailField(max_length=124)
    password = serializers.CharField(
        write_only=True,
        max_length=128,
        style={"input_type": "password"},
    )
