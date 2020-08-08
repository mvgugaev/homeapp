from rest_framework import serializers
from django.contrib.auth.models import User
from .models import *
from workflow.models import Workflow

from workflow.serializers import WorkflowSerializer
from user.serializers import UserSerializer

class TaskWorkflowSerializer(serializers.Serializer):
    id = serializers.IntegerField(label='ID')
    name = serializers.CharField()

    class Meta:
        model = Workflow
        fields = ("id", "name")  

class TaskSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=200)
    users_order = serializers.CharField()
    mode = serializers.CharField()
    delay = serializers.IntegerField()

    workflow = WorkflowSerializer(read_only=True)
    users = UserSerializer(read_only=True, many=True)

    change_order_date = serializers.DateTimeField(format="%d:%m:%Y %H:%M")
    created_at = serializers.DateTimeField(format="%d:%m:%Y %H:%M")
    updated_at = serializers.DateTimeField(format="%d:%m:%Y %H:%M")

    class Meta:
        model = Task