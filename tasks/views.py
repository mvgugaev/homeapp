from django.http import Http404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from .models import *
from .serializers import *
from workflow.models import Workflow

class TaskView(APIView):

    permission_classes = (IsAuthenticated,)

    def get_workflow(self, user, id):
        try:
            return Workflow.objects.get(id=id, users__id__exact=user.id)
        except Workflow.DoesNotExist:
            raise Http404


    def get_workflow_user(self, id, workflow):
        try:
            user = User.objects.get(id=id)

            if user not in workflow.users:
                raise Http404

            return user
        except Workflow.DoesNotExist:
            raise Http404

    def get(self, request, workflow_id=None):
        
        # Empty tasks queryset
        tasks = Task.objects.none()

        if workflow_id:
            workflow = slef.get_workflow(workflow_id, request.user)

            tasks = Task.objects.filter(workflow = workflow)
        else:
            accept_workflows = Workflow.objects.filter(owner = self.request.user) | Workflow.objects.filter(users__id__exact=self.request.user.id)

            for workflow in accept_workflows:
                tasks = tasks | Task.objects.filter(workflow = workflow)

        serializer = TaskSerializer(tasks, many=True)
        return Response({"tasks": serializer.data})

    def post(self, request):

        task = request.data.get('task')
        serializer = TaskSerializer(data=task, context={'request': request})

        if serializer.is_valid(raise_exception=True):
            task_saved = serializer.save()
            task_saved.users.add(*serializer.users)
            task_saved.save()

        return Response({"success": "Task '{}' created successfully".format(task_saved.name)})