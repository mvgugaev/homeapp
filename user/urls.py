from django.urls import path
from . import views

app_name = "user"

# app_name will help us do a reverse look-up latter.
urlpatterns = [
    path('login/', views.login),
    path('api/login/', views.LoginAPIView.as_view()),
]