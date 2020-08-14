from rest_framework import serializers
from django.contrib.auth.models import User
from .models import *
from workflow.models import Workflow

from workflow.serializers import WorkflowSerializer
from user.serializers import UserSerializer

import json

BASE_DATETIME_FORMAT = "%d.%m.%Y %H:%M"

class TaskWorkflowSerializer(serializers.Serializer):
    id = serializers.IntegerField(label='ID')
    name = serializers.CharField()

    class Meta:
        model = Workflow
        fields = ("id", "name")


class TaskChangeHistorySerializer(serializers.Serializer):
    user = UserSerializer()
    description = serializers.CharField()
    type = serializers.CharField()
    created_at = serializers.DateTimeField(format=BASE_DATETIME_FORMAT, read_only=True)

    class Meta:
        model = Workflow


class TaskSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=200)
    users_order = serializers.CharField(required=False, allow_blank=True)
    mode = serializers.CharField()
    delay = serializers.IntegerField(required=False)
    cycle = serializers.IntegerField(required=False)
    use_retry_fail_executor = serializers.BooleanField(required=False)
    description = serializers.CharField()

    workflow_id = serializers.CharField(required=False)
    workflow = WorkflowSerializer(read_only=True)
    users = UserSerializer(many=True)
    executor = UserSerializer(read_only=True)

    last_date = serializers.DateTimeField(format=BASE_DATETIME_FORMAT, input_formats=[BASE_DATETIME_FORMAT], required=False)
    change_order_date = serializers.DateTimeField(format=BASE_DATETIME_FORMAT, input_formats=[BASE_DATETIME_FORMAT], required=False)
    created_at = serializers.DateTimeField(format=BASE_DATETIME_FORMAT, read_only=True)
    updated_at = serializers.DateTimeField(format=BASE_DATETIME_FORMAT, read_only=True)

    compleated = serializers.BooleanField(read_only=True)
    closed = serializers.BooleanField(read_only=True)

    to_retry_count_day = serializers.IntegerField(read_only=True)

    def get_workflow(self, user, id):
        try:
            return Workflow.objects.get(id=id, users__id__exact=user.id)
        except Workflow.DoesNotExist:
            raise Http404

    def get_workflow_user(self, id, workflow):
        try:
            user = User.objects.get(id=id)

            if user not in workflow.users.all():
                raise Http404

            return user
        except Workflow.DoesNotExist:
            raise Http404

    def create(self, validated_data):
        workflow_id = validated_data.pop('workflow_id')
        workflow = self.get_workflow(self.context['request'].user, workflow_id)
        validated_data['workflow'] = workflow
        user_list, user_ordering = [], []
        
        for user_data in validated_data.pop('users', []):
            user_list.append(self.get_workflow_user(user_data['id'], workflow))
            user_ordering.append(user_data['id'])
        
        validated_data['users_order'] = json.dumps(user_ordering)

        self.users = user_list

        return Task.objects.create(**validated_data)

    
    class Meta:
        model = Task