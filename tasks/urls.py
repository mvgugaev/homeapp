from django.urls import path
from .views import TaskView

app_name = "tasks"

# app_name will help us do a reverse look-up latter.
urlpatterns = [
    path('api/', TaskView.as_view()),
    path('api/<int:task_id>', TaskView.as_view()),
]