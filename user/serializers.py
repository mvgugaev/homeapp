from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from .errors import *
from .models import *

class UserSerializer(serializers.Serializer):
    id = serializers.IntegerField(label='ID')
    username = serializers.CharField(required=False)
    email = serializers.CharField(required=False)

    class Meta:
        model = User
        fields = ("id", "username", "email")


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(write_only=True)
    password = serializers.CharField(max_length=128, write_only=True)

    def validate(self, data):
        """
        Validates user data.
        """
        email = data.get('email', None)
        password = data.get('password', None)

        if email is None:
            raise serializers.ValidationError(EMPTY_EMAIL)

        if password is None:
            raise serializers.ValidationError(EMPTY_PASSWORD)

        self.user = authenticate(username=email, password=password)

        if self.user is None:
            raise serializers.ValidationError(USER_DOES_NOT_EXIST)

        return {'status': True}
  