import datetime

from django.contrib.auth import get_user_model
from django.db.models import Q
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
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


class WorkerDetailView(generic.DetailView):
    model = get_user_model()
    template_name = "tasks/profile_page.html"
    context_object_name = "profile_list"
    queryset = get_user_model().objects.filter()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        to_do_tasks = Task.objects.filter(assignees__in=[kwargs["object"]], in_progress=False)
        in_progress_tasks = Task.objects.filter(assignees__in=[kwargs["object"]], in_progress=True)
        context["to_do_tasks"] = to_do_tasks
        context["in_progress_tasks"] = in_progress_tasks
        return context


def task_list(request, pk):
    to_do_tasks = Task.objects.filter(in_progress=False, assignees__in=[pk], is_completed=False)
    in_progress_tasks = Task.objects.filter(in_progress=True, assignees__in=[pk], is_completed=False)
    completed_tasks = Task.objects.filter(is_completed=True)

    if request.method == 'POST':
        if request.POST.get("task_id_done"):
            task_id = request.POST.get('task_id_done')
            task = Task.objects.get(id=task_id)
            task.is_completed = True
            task.in_progress = False
            task.completed_time = datetime.datetime.now()
        elif request.POST.get("task_id"):
            task_id = request.POST.get('task_id')
            task = Task.objects.get(id=task_id)
            task.in_progress = True
        task.save()
        return HttpResponseRedirect(request.path_info)

    context = {
        'to_do_tasks': to_do_tasks,
        'in_progress_tasks': in_progress_tasks,
        "completed_tasks": completed_tasks,
    }

    return render(request, 'tasks/profile_page.html', context)
