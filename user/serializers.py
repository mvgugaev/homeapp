from rest_framework import serializers
from django.contrib.auth.models import User
from .models import *

class UserSerializer(serializers.Serializer):
    id = serializers.IntegerField(label='ID')
    username = serializers.CharField()
    email = serializers.CharField()

    class Meta:
        model = User
        fields = ("id", "username", "email")
  