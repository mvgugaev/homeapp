from django.http import Http404
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import *
from .serializers import *
from workflow.models import Workflow

class TaskView(APIView):

    def get_workflow(self, user, id):
        try:
            return Workflow.objects.get(id=id, users__id__exact=user.id)
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