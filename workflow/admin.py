from django.contrib import admin
from .models import *

@admin.register(Workflow)
class WorkflowAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'created_at', 'updated_at')
    filter_horizontal = ('users',)
