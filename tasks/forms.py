from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Q
from django.forms.widgets import DateTimeInput

from tasks.models import Task, Worker


class CreateTaskForm(forms.ModelForm):
    assignees = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.filter(~Q(first_name="")),
        widget=forms.CheckboxSelectMultiple,
        required=True,
    )

    class Meta:
        model = Task
        fields = [
            "name",
            "description",
            "deadline",
            "priority",
            "task_type",
            "assignees",
        ]
        widgets = {"deadline": DateTimeInput(attrs={"type": "datetime-local"})}


class CreateWorkerForm(UserCreationForm):
    first_name = forms.CharField(
        max_length=255, required=True, label="First name"
    )
    last_name = forms.CharField(
        max_length=255, required=True, label="Last name"
    )

    class Meta(UserCreationForm.Meta):
        model = Worker
        fields = UserCreationForm.Meta.fields + (
            "first_name",
            "last_name",
            "email",
            "position",
        )
