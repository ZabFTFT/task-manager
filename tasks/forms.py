from django import forms
from django.contrib.auth import get_user_model
from django.forms.widgets import DateTimeInput

from tasks.models import Task


class CreateTaskForm(forms.ModelForm):
    assignees = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True,
    )

    class Meta:
        model = Task
        fields = ["name", "description", "deadline", "priority", "task_type", "assignees"]
        widgets = {
            "deadline": DateTimeInput(attrs={
                "type": "datetime-local"
            })
        }
