from django.db import models
from django.contrib.auth.models import User

# Profile user to store addition information
class Profile(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="User")
    avatar = models.ImageField(verbose_name="User avatar")

    # Meta fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Profile"
        verbose_name_plural = "Profiles"

    def __str__(self):
        return '{0} [{1}]'.format(self.user.email)
