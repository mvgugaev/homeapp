from django.http import Http404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from .models import *
from .serializers import *
from .errors import *
from workflow.models import Workflow

class TaskView(APIView):

    permission_classes = (IsAuthenticated,)
    serializer_class = TaskSerializer
    accept_post_methods = ('create', 'exec', 'close', 'delete')

    def get_workflow(self, user, id):
        try:
            return Workflow.objects.get(id=id, users__id__exact=user.id)
        except Workflow.DoesNotExist:
            raise Http404

    def get_task(self, user, id):
        try:
            task = Task.objects.get(id=id)

            if task.workflow.owner != user and user not in task.workflow.users.all():
                raise Http404

            return task
        except Task.DoesNotExist:
            raise Http404


    def get_workflow_user(self, id, workflow):
        try:
            user = User.objects.get(id=id)

            if user not in workflow.users:
                raise Http404

            return user
        except Workflow.DoesNotExist:
            raise Http404

    

    def get(self, request, task_id=None):

        workflow_id = self.request.query_params.get('workflow_id', None)
        
        # Empty tasks queryset
        tasks = Task.objects.none()

        # Additional filter
        query_filters = {}

        if task_id:
            query_filters['id'] = task_id

        if workflow_id:
            workflow = self.get_workflow(request.user, workflow_id)

            tasks = Task.objects.filter(workflow = workflow, **query_filters)
        else:
            accept_workflows = Workflow.objects.filter(owner = self.request.user) | Workflow.objects.filter(users__id__exact=self.request.user.id)

            for workflow in accept_workflows:
                tasks = tasks | Task.objects.filter(workflow = workflow, **query_filters)

        tasks = tasks.order_by('-created_at')

        serializer = self.serializer_class(tasks, many=True)
        return Response({"tasks": serializer.data})

    def post(self, request):

        method_type = request.data.get('type', None)
        task = request.data.get('task', None)

        if not method_type or method_type not in self.accept_post_methods:
            raise serializers.ValidationError(UNDEFINED_METHOD)

        if not task:
            raise serializers.ValidationError(UNDEFINED_TASK_PARAM)

        if method_type == 'create':
            serializer = self.serializer_class(data=task, context={'request': request})

            if serializer.is_valid(raise_exception=True):
                task_saved = serializer.save()
                task_saved.users.add(*serializer.users)
                task_saved.save()
                task_saved.set_executor_by_order()
                task_saved.save()

            return Response({"success": "Task '{}' created successfully".format(task_saved.name)})
        
        elif method_type == 'exec':
            
            task_id = task.get('id', None)

            if not task_id:
                raise serializers.ValidationError(TASK_ID_REQUIRED)

            task = self.get_task(request.user, task_id)
            task.exec_task()

            return Response({"success": "Task '{}' compleated successfully".format(task.name)})