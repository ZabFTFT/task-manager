from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from tasks.models import Task


def index(request: HttpRequest) -> HttpResponse:
    num_task_all = Task.objects.count()
    num_task_in_progress = Task.objects.filter(in_progress=True)

    context = {
        "num_task_all": num_task_all,
        "num_task_in_progress": num_task_in_progress,
    }

    return render(request, "tasks/index.html", context=context)
