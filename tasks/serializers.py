from rest_framework import serializers
from django.contrib.auth.models import User
from .models import *
from workflow.models import Workflow

from workflow.serializers import WorkflowSerializer
from user.serializers import UserSerializer

BASE_DATETIME_FORMAT = "%d:%m:%Y %H:%M"

class TaskWorkflowSerializer(serializers.Serializer):
    id = serializers.IntegerField(label='ID')
    name = serializers.CharField()

    class Meta:
        model = Workflow
        fields = ("id", "name")  

class TaskSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=200)
    users_order = serializers.CharField(required=False, allow_blank=True)
    mode = serializers.CharField()
    delay = serializers.IntegerField()

    workflow_id = serializers.CharField(required=False)
    workflow = WorkflowSerializer(read_only=True)
    users = UserSerializer(many=True)

    change_order_date = serializers.DateTimeField(format=BASE_DATETIME_FORMAT, input_formats=[BASE_DATETIME_FORMAT])
    created_at = serializers.DateTimeField(format=BASE_DATETIME_FORMAT, input_formats=[BASE_DATETIME_FORMAT])
    updated_at = serializers.DateTimeField(format=BASE_DATETIME_FORMAT, input_formats=[BASE_DATETIME_FORMAT])

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
        user_list = []
        
        for user_data in validated_data.pop('users', []):
            user_list.append(self.get_workflow_user(user_data['id'], workflow))
        
        self.users = user_list

        return Task.objects.create(**validated_data)

    
    class Meta:
        model = Task