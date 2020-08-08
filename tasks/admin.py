from django.contrib import admin
from .models import *

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('name', 'workflow', 'created_at', 'mode')
    filter_horizontal = ('users',)

@admin.register(TaskChangeHistory)
class TaskChangeHistoryAdmin(admin.ModelAdmin):
    list_display = ('task', 'user', 'type', 'created_at')

