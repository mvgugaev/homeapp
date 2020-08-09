from django.urls import path
from . import views

app_name = "workflow"

# app_name will help us do a reverse look-up latter.
urlpatterns = [
    path('api/', views.WorkflowView.as_view()),
    path('<int:workflow_id>/', views.workflow),
    path('', views.workflows),
]