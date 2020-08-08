from django.urls import path
from .views import TaskView

app_name = "tasks"

# app_name will help us do a reverse look-up latter.
urlpatterns = [
    path('', TaskView.as_view()),
]