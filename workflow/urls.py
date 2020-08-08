from django.urls import path
from .views import WorkflowView

app_name = "workflow"

# app_name will help us do a reverse look-up latter.
urlpatterns = [
    path('', WorkflowView.as_view()),
]