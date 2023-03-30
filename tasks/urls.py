from django.urls import path

from tasks.views import (
    index,
    ProjectTaskListView,
    CreateTaskView,
    personal_task_list,
    ProjectTaskDetailView,
    CreateWorkerView,
    DeleteTaskView,
    ProjectTaskListFinishedView,
)

app_name = "tasks"

urlpatterns = [
    path("", index, name="index"),
    path("project_tasks/", ProjectTaskListView.as_view(), name="project-tasks-list"),
    path("create_task/", CreateTaskView.as_view(), name="create-task"),
    path("my_tasks/<int:pk>/", personal_task_list, name="my-tasks"),
    path("project_tasks/<int:pk>/", ProjectTaskDetailView.as_view(), name="project-task-detail"),
    path("create_worker/", CreateWorkerView.as_view(), name="worker-create"),
    path("project_tasks/<int:pk>/delete", DeleteTaskView.as_view(), name="task-delete"),
    path("project_tasks/finished/", ProjectTaskListFinishedView.as_view(), name="project-tasks-finished" )



]