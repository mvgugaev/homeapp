from django.db import models
from workflow.models import *

# Workflow task model
class Task(models.Model):

    MODE = (
        ('0', 'Single'),
        ('1', 'Repeat'),
        ('2', 'Repeat with time'),
        ('3', 'Repeat with order'),
        ('4', 'Repeat with order and time')
    )

    name = models.CharField(max_length=200, verbose_name="Title")
    workflow = models.ForeignKey(Workflow, on_delete=models.CASCADE, verbose_name="Workflow")
    users = models.ManyToManyField(User, related_name="task_users", verbose_name="User added to task")

    users_order = models.TextField(null=True, blank=True, verbose_name="Execute task users order")
    mode = models.CharField(
        max_length=1,
        choices=MODE,
        default=MODE[0][0],
    )

    change_order_date = models.DateTimeField(auto_now_add=True, verbose_name="Change order")
    delay = models.IntegerField(default=0, verbose_name="Task delay")

    # Meta fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Task"
        verbose_name_plural = "Tasks"

    def __str__(self):
        return '{0} [{1}]'.format(self.name, self.workflow.name)


# Workflow task history model
class TaskChangeHistory(models.Model):

    TYPE = (
        ('0', 'Create'),
        ('1', 'Change params'),
        ('2', 'Execute')
    )

    type = models.CharField(
        max_length=1,
        choices=TYPE,
        default=TYPE[0][0],
    )

    task = models.ForeignKey(Task, on_delete=models.CASCADE, verbose_name="Task")
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="User")
    description = models.TextField(null=True, blank=True, verbose_name="Change description")

    # Meta fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Task history"
        verbose_name_plural = "Tasks history"

    def __str__(self):
        return '{0} [{1}]'.format(self.user.email, self.task.name)

