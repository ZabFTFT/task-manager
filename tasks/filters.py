import django_filters
from django.contrib.auth import get_user_model
from django.db.models import Q
from django_filters import (
    DateFilter,
    ModelMultipleChoiceFilter,
    CharFilter,
)

from django import forms


from tasks.models import Task


class OrderFilter(django_filters.FilterSet):
    task_name = CharFilter(
        field_name="name",
        lookup_expr="icontains",
        label="Task name"
    )
    deadline_date = DateFilter(
        field_name="deadline",
        lookup_expr="lte",
        widget=forms.widgets.DateInput(attrs={'type': 'date'}),
        label="Deadline date"
    )
    assignees = ModelMultipleChoiceFilter(
        queryset=get_user_model().objects.filter(~Q(first_name="")),
        widget=forms.CheckboxSelectMultiple(),
        label="Participants"
    )

    class Meta:
        model = Task
        fields = ['task_name', 'in_progress', 'task_type', 'priority', 'deadline_date', 'assignees']


