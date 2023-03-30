import datetime
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone


class Position(models.Model):
    name = models.CharField(max_length=63)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class TaskType(models.Model):
    name = models.CharField(max_length=63)

    def __str__(self):
        return self.name


class Worker(AbstractUser):
    position = models.ForeignKey(Position, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.first_name} {self.last_name} {self.position}"


class Task(models.Model):
    task_priority = [
        ("C", "Critical"),
        ("H", "High"),
        ("M", "Medium"),
        ("L", "Low"),
    ]

    name = models.CharField(max_length=255)
    description = models.TextField()
    deadline = models.DateTimeField()
    is_completed = models.BooleanField(default=False)
    completed_time = models.DateTimeField(null=True, default=None)
    in_progress = models.BooleanField(default=False)
    priority = models.CharField(max_length=1, choices=task_priority)
    task_type = models.ForeignKey(TaskType, on_delete=models.CASCADE)
    assignees = models.ManyToManyField(settings.AUTH_USER_MODEL)

    class Meta:
        default_related_name = "tasks"
        ordering = ["deadline"]

    def clean(self, *args, **kwargs):
        # run the base validation
        super().clean(*args, **kwargs)
        now = timezone.now()
        # Don't allow dates older than now.
        if self.deadline < now:
            raise ValidationError("Deadline date must be later than now.")
