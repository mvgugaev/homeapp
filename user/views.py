from django.shortcuts import render
from django.http import HttpResponseRedirect
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from django.contrib.auth import login as django_login
from .serializers import *


def login(request):

    if request.user.is_authenticated:
        return HttpResponseRedirect('/workflows/')

    render_contect = {
        'page_without_layout': True
    }

    return render(request, 'user/login.html', render_contect)


class LoginAPIView(APIView):
    """
    Logs in an existing user.
    """
    permission_classes = (AllowAny,)

    def post(self, request):
        """
        Checks is user exists.
        Email and password are required.
        """
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        django_login(request, serializer.user)

        return Response(serializer.data, status=status.HTTP_200_OK)