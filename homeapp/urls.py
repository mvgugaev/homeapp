from django.contrib import admin
from django.urls import path, include


# Base app urls scheme:
# /user/* - pages
# /user/api/* - django rest
# ..........

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/', include('user.urls')),
    path('api/workflows/', include('workflow.urls')),
    path('api/tasks/', include('tasks.urls')),
]
