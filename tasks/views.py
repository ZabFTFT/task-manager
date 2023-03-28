from django.db.models import Q
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views import generic

from tasks.forms import CreateTaskForm
from tasks.models import Task


def index(request: HttpRequest) -> HttpResponse:
    num_task_all = Task.objects.count()
    num_task_in_progress = Task.objects.filter(in_progress=True).count()

    context = {
        "num_task_all": num_task_all,
        "num_task_in_progress": num_task_in_progress,
    }

    return render(request, "tasks/index.html", context=context)


class ToDoList(generic.ListView):
    model = Task
    queryset = Task.objects.filter(is_completed=False, in_progress=False)
    template_name = "tasks/todo_list.html"
    context_object_name = "todo_list"

class CreateTaskView(generic.CreateView):
    form_class = CreateTaskForm
    template_name = "tasks/create_task.html"



