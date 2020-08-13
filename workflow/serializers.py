from rest_framework import serializers
from django.contrib.auth.models import User
from .models import *

from user.serializers import UserSerializer


class WorkflowSerializer(serializers.Serializer):
    owner = UserSerializer(read_only=True)
    users = UserSerializer(read_only=True, many=True)
    id = serializers.IntegerField(label='ID', read_only=True)
    name = serializers.CharField(max_length=200)
    created_at = serializers.DateTimeField(format="%d:%m:%Y %H:%M")
    updated_at = serializers.DateTimeField(format="%d:%m:%Y %H:%M")

    class Meta:
        model = Workflow
        fields = ("id", "name", "created_at", "updated_at")



class WorkflowUserRequestSerializer(serializers.Serializer):
    workflow_id = serializers.CharField(required=False)
    email = serializers.CharField(max_length=200)
    accepted = serializers.CharField(read_only=True)

    class Meta:
        model = WorkflowUserRequest