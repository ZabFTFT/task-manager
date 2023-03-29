import datetime

from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic

from tasks.filters import OrderFilter
from tasks.forms import CreateTaskForm, CreateWorkerForm
from tasks.models import Task


def index(request: HttpRequest) -> HttpResponse:
    num_task_all = Task.objects.count()
    num_task_in_progress = Task.objects.filter(in_progress=True).count()

    context = {
        "num_task_all": num_task_all,
        "num_task_in_progress": num_task_in_progress,
    }

    return render(request, "tasks/index.html", context=context)


class ProjectTasksList(generic.ListView):
    model = Task
    template_name = "tasks/all_tasks.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        tasks = Task.objects.filter(is_completed=False)
        myFilter = OrderFilter(self.request.GET, queryset=tasks)
        tasks_filter = myFilter.qs
        context["filter"] = myFilter
        context["tasks"] = tasks
        context["tasks_filter"] = tasks_filter
        return context


class CreateTaskView(generic.CreateView):
    form_class = CreateTaskForm
    template_name = "tasks/create_task.html"
    success_url = reverse_lazy("tasks:project-tasks-list")


class DeleteTaskView(generic.DeleteView):
    model = Task
    template_name = "tasks/task_delete_confirm.html"
    success_url = reverse_lazy("tasks:project-tasks-list")


class ProjectTaskDetailView(generic.DetailView):
    model = Task
    template_name = "tasks/project_task.html"
    context_object_name = "project_task"


class CreateWorkerView(generic.CreateView):
    form_class = CreateWorkerForm
    template_name = "tasks/create_worker.html"
    success_url = reverse_lazy("tasks:worker-create")


def personal_task_list(request, pk):
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
