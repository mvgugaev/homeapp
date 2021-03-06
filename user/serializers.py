from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from .errors import *
from .models import *

class UserSerializer(serializers.Serializer):
    id = serializers.IntegerField(label='ID')
    username = serializers.CharField(required=False)
    email = serializers.CharField(required=False)
    avatar_url = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ("id", "username", "email")

    def get_avatar_url(self, obj):
        profile = Profile.objects.get(user=obj)
        return profile.avatar.url if profile.avatar else '/static/images/default_avatar.png'


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
  