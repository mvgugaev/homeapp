from django.contrib import admin
from .models import *

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('get_user_email', )

    def get_user_email(self, obj):
        return obj.user.email

