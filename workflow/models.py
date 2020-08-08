from django.db import models
from django.contrib.auth.models import User

# Main user dashboard
class Workflow(models.Model):
    name = models.CharField(max_length=200, verbose_name="Title")
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Owner")
    users = models.ManyToManyField(User, related_name="users", verbose_name="User with workflow access")

    # Meta fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Workflow"
        verbose_name_plural = "Workflows"

    def __str__(self):
        return '{0} [{1}]'.format(self.name, self.owner.email)

