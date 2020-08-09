from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from .models import *
from .serializers import *

class WorkflowView(APIView):

    permission_classes = (IsAuthenticated,)

    def get(self, request):

        workflows = Workflow.objects.filter(owner = self.request.user) | Workflow.objects.filter(users__id__exact=self.request.user.id)
        serializer = WorkflowSerializer(workflows, many=True)
        return Response({"workflows": serializer.data})