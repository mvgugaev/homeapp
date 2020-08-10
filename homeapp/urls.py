from django.contrib import admin
from django.views.generic.base import RedirectView
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static


# Base app urls scheme:
# /user/* - pages
# /user/api/* - django rest
# ..........

urlpatterns = [
    path('', RedirectView.as_view(url='/workflows/')),
    path('admin/', admin.site.urls),
    path('user/', include('user.urls')),
    path('workflows/', include('workflow.urls')),
    path('tasks/', include('tasks.urls')),
]  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
