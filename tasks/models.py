from django.db import models
from workflow.models import *
from django.contrib.auth.models import User
from datetime import datetime
import json

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
    description = models.TextField(null=True, blank=True, verbose_name="Description")
    workflow = models.ForeignKey(Workflow, on_delete=models.CASCADE, verbose_name="Workflow")
    users = models.ManyToManyField(User, related_name="task_users", verbose_name="User added to task")
    executor = models.ForeignKey(User, null=True, on_delete=models.CASCADE, verbose_name="Executor")
    
    users_order = models.TextField(null=True, blank=True, verbose_name="Execute task users order", default="[]")
    mode = models.CharField(
        max_length=1,
        choices=MODE,
        default=MODE[0][0],
    )

    change_order_date = models.DateTimeField(verbose_name="Change order")
    last_date = models.DateTimeField(verbose_name="Compleate date limit")
    delay = models.IntegerField(default=0, verbose_name="Task delay")
    cycle = models.IntegerField(default=0, verbose_name="Hours of cycle")

    compleated = models.BooleanField(default=False, verbose_name="Is compleated")
    closed = models.BooleanField(default=False, verbose_name="Is closed")

    # Meta fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Task"
        verbose_name_plural = "Tasks"

    def __str__(self):
        return '{0} [{1}]'.format(self.name, self.workflow.name)

    def save(self, *args, **kwargs): 
        self.change_order_date = datetime.now()
        super(Task, self).save(*args, **kwargs)

    def set_executor_by_order(self):
        order = json.loads(self.users_order)

        if len(order) > 0:
            executor = self.users.all().get(id=order[0])

            if self.executor != executor:
                self.executor = executor

    def set_next_executor(self):
        
        order = json.loads(self.users_order)

        if len(order) > 1:
            order = order[1:] + order[:1]

            self.users_order = json.dumps(order)
            self.set_executor_by_order()
        
            self.save()

    def exec_task(self):

        if self.mode in ('0', '2', '4'):
            self.compleated = True

        if self.mode == '3':
            self.set_next_executor()

        if self.delay > 0:
            self.delay -= 1

        self.save()

    def change_task_status(self, closed: bool):
        self.closed = closed
        self.save()

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

